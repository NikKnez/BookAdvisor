### Book Advisor 📚

#### Overview
Book Advisor is a web application that offers personalized book recommendations based on users reading preferences. Leveraging data from the New York Times Bestseller lists and integrating with the Google Books API, Book Advisor provides a seamless experience for discovering new reads. The system consists of both frontend and backend components, with the frontend built using React.js and the backend powered by Flask.

#### Features
- View current New York Times bestsellers for both fiction and nonfiction.
- Receive tailored book recommendations based on your reading history.
- Search for books by title, author, or genre.
- Access detailed book information including cover images, ratings, and publication details.
- Save favorite books to your profile for future reference.

### Backend (BookAdvisor)

#### Prerequisites
- Python 3.10.x or later
- `venv` module version 3.3 or later
- MongoDB installed and running locally

#### Setup
1. Navigate to the `BookAdvisor` directory.
2. Create a virtual environment using `python -m venv .` and activate it.
3. Install dependencies using `pip install -r requirements.txt`.
4. Set environment variables for database credentials, mail server details, Google Books API key (https://developers.google.com/books), and New York Times API key (https://developer.nytimes.com/).
5. Run the Flask server using `python app.py`.

### Frontend (book_advisor_frontend)

#### Prerequisites
- Node.js 16.x and npm

#### Development
1. Navigate to the `book_advisor_frontend` (https://github.com/NikKnez/book_advisor_frontend) directory.
2. Install dependencies using `npm install`.
3. Set the `REACT_APP_API_ENDPOINT` variable in the `.env` file to the URL of the backend server (by default this is `http://127.0.0.1:5000/`).
4. Start the development server using `npm start`.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any enhancements or bug fixes.


**Developed by [NikKnez](https://github.com/NikKnez)**
