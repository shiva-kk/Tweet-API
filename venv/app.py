import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load tweet data from the JSON file
with open('100tweets.json', 'r') as file:
    tweets_data = json.load(file)

# Step 2: Hello World Endpoint
@app.route('/')
def hello_world():
    return 'Hello World.'

# Step 3: All Tweets Endpoint
@app.route('/tweets', methods=['GET'])
def get_all_tweets():
    global tweets_data  # Ensure that tweets_data is considered global
    # Step 4: Filter tweets based on a query parameter (optional)
    query_param = request.args.get('filter')
    if query_param:
        filtered_tweets = [tweet for tweet in tweets_data if query_param.lower() in tweet['text'].lower()]
        return jsonify(filtered_tweets)

    return jsonify(tweets_data)

# Step 5: Get a Specific Tweet by ID
@app.route('/tweet/<int:tweet_id>', methods=['GET'])
def get_tweet_by_id(tweet_id):
    try:
        tweet = next(tweet for tweet in tweets_data if tweet['id_str'] == tweet_id)
        return jsonify(tweet)
    except StopIteration:
        return jsonify({'error': 'Tweet not found'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid tweet ID format'}), 400

# Step 6: Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    app.run(debug=True)


# Test Hello World endpoint
#curl http://localhost:5000/

# Test All Tweets endpoint
#curl http://localhost:5000/tweets

# Test Filtered Tweets endpoint with escaped characters
#curl http://localhost:5000/tweets\?filter\=texas

# Test Specific Tweet endpoint
#curl http://localhost:5000/tweet/1360000000000000000