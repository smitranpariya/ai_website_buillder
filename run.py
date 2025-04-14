from app import create_app

# Create the Flask app instance using the factory function
app = create_app()
print(app.url_map)

@app.route('/')
def home():
    return "Flask is alive!"

if __name__ == "__main__":
    # Run the app locally on port 5000
    app.run(debug=True, host="0.0.0.0", port=5001)
