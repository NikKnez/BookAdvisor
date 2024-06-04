from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from user_auth import token_val
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rake_nltk import Rake
from search import search_books

RECOMMENDER = Blueprint("rec", __name__)


def get_book_info(book):
    resp = book["title"]
    if book["summary"] != "No summary available":
        resp += " " + book["summary"]
    if book["categories"] != "No category available":
        resp += " " + book["categories"]
    if book["authors"] != "No author available":
        resp += " " + book["authors"]
    return resp


@RECOMMENDER.route("/rec", methods=["GET"])
def gen_recomm():
    token = request.args.get("token")

    # Validate users token
    data = token_val(token)
    if data is None:
        return jsonify({"message": "Invalid token"}), 400

    # Find user in database
    user_id = data["_id"]
    users = current_app.config["DATABASE"]["users"]
    user = users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        return jsonify({"message": "user id not present in database"}), 402

    # Get users most recently read book
    recent_read = user["main_collection"]
    if len(recent_read) == 0:
        return jsonify({"message": "No books read so far!"}), 400

    recent_read = user["main_collection"][0]
    recent_read = current_app.config["DATABASE"]["books"].find_one(
        {"book_id": recent_read["book_id"]}
    )

    # Use rake-nltk to extract keywords from book info
    r = Rake()

    if recent_read["summary"] == "No summary available":
        info = recent_read["title"]
    else:
        info = recent_read["summary"]

    r.extract_keywords_from_text(info)
    main_word = r.get_ranked_phrases()[0]

    # Search for relevant books in both the cache and googlebooks
    potential_recs, status_code = search_books(
        main_word, current_app.config["DATABASE"]["books"]
    )

    # Filter potential recommendations
    books_read_itr = current_app.config["DATABASE"]["books_read"].find(
        {"user_id": user_id}, {"_id": 0, "book_id": 1}
    )
    books_read = [book["book_id"] for book in books_read_itr]

    filtered_recs = []
    for book in potential_recs:
        if book["book_id"] not in books_read and book["title"] not in [rec["title"] for rec in filtered_recs]:
            filtered_recs.append(book)

    # Append the most recently read book once
    filtered_recs.append(recent_read)

    # Create "info" field for each book
    for book in filtered_recs:
        book["info"] = get_book_info(book)

    # Calculate similarity ranking between all books
    data = pd.DataFrame(filtered_recs)
    data = data[["title", "info", "book_id"]]

    feature = data["info"].tolist()
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(feature)

    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(data.index, index=data["book_id"]).drop_duplicates()

    # Perform recommendation logic
    index = indices[recent_read["book_id"]]
    sim_scores = list(enumerate(similarity[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]

    recs = data["book_id"].iloc[book_indices]

    # List to store non-duplicate recommended books
    non_duplicate_recs = []

    for rec in recs:
        for book in filtered_recs:
            if book["book_id"] == rec:
                non_duplicate_recs.append(book)
                break

    # Return the final list of recommendations
    return jsonify({"rec": non_duplicate_recs}), 200
