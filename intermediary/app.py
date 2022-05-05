# ------------Backend module---------------
from flask import Flask, request, make_response
from flask_cors import CORS

# ------------Utils----------------
from utils.shopee_crawler import ShopeeCrawler
from utils.statistic import SummaryStatistic, SentimentStatistic
from utils.load_json_template import LoadJSONTemplate
from utils.sentiment_predict import SentimentPredict
from utils.data_preparation import DataPreprocess
from utils.timing import timming


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
json_template = LoadJSONTemplate()
json_template.load()
failure_json_template = json_template.get_failure_json_template()

@app.route("/")
def landing():
    return "Server is working!"

@app.route("/api/getAspectDefinition", endpoint='getAspect', methods = ['GET'])
@timming
def getAspect():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            # Load
            json_template.set_aspect_definition_template()
            aspect_definition_json = json_template.get_aspect_definition_template()
            # Response
            response = make_response(aspect_definition_json)
            response.headers["Content-Type"] = "application/json"
            return response
        except:
            response = make_response(failure_json_template)
            return response
    else:
        return 'Content-Type not supported!'

@app.route("/api/shopee/getCommentCrawler/<int:shop_id>/<int:item_id>",  endpoint='crawlComments', methods=['GET'])
@timming
def crawlComments(shop_id, item_id):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            # Crawler
            comments, is_entire = ShopeeCrawler().getComments(item_id, shop_id)
            json_template.set_get_comments_template(comments, is_entire, len(comments))
            get_comments_json = json_template.get_get_comments_template()
            # Response
            response = make_response(get_comments_json)
            response.headers["Content-Type"] = "application/json"
            return response
        except:
            response = make_response(failure_json_template)
            return response
    else:
        return 'Content-Type not supported!'

@app.route("/api/shopee/commentsPreprocess", endpoint='preprocessComments', methods=['POST'])
@timming
def preprocessComments():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            # Summary
            content = request.get_json()
            product_type_id = content.get('productTypeId')
            comments = content.get('comments', False)
            preprocessed_data = DataPreprocess(product_type_id, comments).run(option='all')
            json_template.set_comment_preprocess_template(preprocessed_data)
            comments_preprocess_json = json_template.get_comments_preprocess_template()
            # Response
            response = make_response(comments_preprocess_json)
            response.headers["Content-Type"] = "application/json"
            return response
        except:
            response = make_response(failure_json_template)
            return response
    else:
        return 'Content-Type not supported!'


@app.route("/api/shopee/getCommentsAnalysisSummary", endpoint='getCommentsAnalysisSummary', methods=['POST'])
@timming
def getCommentsAnalysisSummary():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            # Summary
            content = request.get_json()
            product_type_id = content.get('productTypeId')
            comments = content.get('comments', False)
            statistic_data = SummaryStatistic(product_type_id, comments).run()
            json_template.set_summary_analysis_template(product_type_id, statistic_data)
            summary_analysis_json = json_template.get_summary_analysis_template()
            # Response
            response = make_response(summary_analysis_json)
            response.headers["Content-Type"] = "application/json"
            return response
        except:
            response = make_response(failure_json_template)
            return response
    else:
        return 'Content-Type not supported!'


@app.route("/api/shopee/getCommentsSentimentSummary", endpoint='getSentimentsAnalysisSummary', methods=['POST'])
@timming
def getSentimentsAnalysisSummary():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            # Summary
            content = request.get_json()
            product_type_id = content.get('productTypeId')
            comments = content.get('comments', False)
            statistic_data = SentimentStatistic(product_type_id, comments).run()
            json_template.set_summary_sentiment_template(product_type_id, statistic_data)
            sentiment_analysis_json = json_template.get_summary_sentiment_template()
            # Response
            response = make_response(sentiment_analysis_json)
            response.headers["Content-Type"] = "application/json"
            return response
        except:
            response = make_response(failure_json_template)
            return response
    else:
        return 'Content-Type not supported!'


@app.route('/api/shopee/getSentiments', endpoint='getSentiments', methods=['POST'])
@timming
def getSentiments():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        try:
            content = request.get_json()
            comments = content.get('comments', False)
            product_type_id = content.get('productTypeId', False)
            # Predict
            result = SentimentPredict(product_type_id, comments).run()
            json_template.set_get_sentiment_template(result)
            get_sentiment_json = json_template.get_get_sentiment_template()
            # Response
            response = make_response(get_sentiment_json)
            response.headers["Content-Type"] = "application/json"
            return response
        except:
            response = make_response(failure_json_template)
            return response
    else:
        return 'Content-Type not supported!'


if __name__ == "__main__":
    print('Server is runnning')
    app.run()
