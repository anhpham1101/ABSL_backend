import json
from copy import deepcopy
from static.aspect_definition import aspect_definition

FAILURE_JSON_TEMPLATE_PATH = f'json_response_template/failure_json_response_template.json'
ASPECT_JSON_TEMPLATE_PATH = f'json_response_template/aspect_definition_response_template.json'
GET_COMMENTS_TEMPLATE_PATH = f'json_response_template/get_comments_template.json'
COMMENTS_PREPROCESS_TEMPLATE_PATH = f'json_response_template/comments_preprocess_template.json'
SUMMARY_ANALYSIS_TEMPLATE_PATH = f'json_response_template/summary_analysis_response_template.json'
SUMMARY_SENTIMENT_TEMPLATE_PATH = f'json_response_template/summary_sentiment_response_template.json'
GET_SENTIMENT_TEMPLATE_PATH = f'json_response_template/get_sentiment_response_template.json'

class LoadJSONTemplate:
    def __init__(self):
        self.failure_json_template = None
        self.aspect_definition_template = None
        self.get_comments_template = None
        self.comments_preprocess_template = None
        self.summary_sentiment_template = None
        self.summary_analysis_template = None
        self.get_sentiment_template = None
        
    def _load_failure_json_template(self):
        f = open(FAILURE_JSON_TEMPLATE_PATH, encoding='utf-8')
        self.failure_json_template = json.load(f)
        f.close()
    
    def _load_aspect_definition_template(self):
        f = open(ASPECT_JSON_TEMPLATE_PATH, encoding='utf-8')
        self.aspect_definition_template = json.load(f)
        f.close()
    
    def _load_get_comments_template(self):
        f = open(GET_COMMENTS_TEMPLATE_PATH, encoding='utf-8')
        self.get_comments_template = json.load(f)
        f.close()

    def _load_comments_preprocess_template(self):
        f = open(COMMENTS_PREPROCESS_TEMPLATE_PATH, encoding='utf-8')
        self.comments_preprocess_template = json.load(f)
        f.close()
    
    def _load_summary_analysis_template(self):
        f = open(SUMMARY_ANALYSIS_TEMPLATE_PATH, encoding='utf-8')
        self.summary_analysis_template = json.load(f)
        f.close()
    
    def _load_summary_sentiment_template(self):
        f = open(SUMMARY_SENTIMENT_TEMPLATE_PATH, encoding='utf-8')
        self.summary_sentiment_template = json.load(f)
        f.close()

    def _load_get_sentiment_template(self):
        f = open(GET_SENTIMENT_TEMPLATE_PATH, encoding='utf-8')
        self.get_sentiment_template = json.load(f)
        f.close()

    def get_failure_json_template(self):
        return self.failure_json_template
    
    def get_aspect_definition_template(self):
        return self.aspect_definition_template

    def get_get_comments_template(self):
        return self.get_comments_template
    
    def get_comments_preprocess_template(self):
        return self.comments_preprocess_template

    def get_get_sentiment_template(self):
        return self.get_sentiment_template

    def get_summary_analysis_template(self):
        return self.summary_analysis_template
    
    def get_summary_sentiment_template(self):
        return self.summary_sentiment_template
    
    def set_aspect_definition_template(self):
        data = deepcopy(aspect_definition)
        for _, value in data.items():
            for asp in value.get('aspect'):
                asp['definition'] = asp.get('definition').replace("\n", "")
        self.aspect_definition_template["json"] = data
    
    def set_get_sentiment_template(self, data):
        self.get_sentiment_template.get("json")["sentiments"] = data
    
    def set_get_comments_template(self, data, is_entire, comments_count):
        if is_entire:
            section_title = "KẾT QUẢ PHÂN TÍCH TỪ %s ĐÁNH GIÁ CÓ BÌNH LUẬN VỀ SẢN PHẨM" % comments_count
        else:
            section_title = "KẾT QUẢ PHÂN TÍCH TỪ %s ĐÁNH GIÁ CÓ BÌNH LUẬN MỚI NHẤT VỀ SẢN PHẨM" % comments_count
        self.get_comments_template.get("json")["sectionTitle"] = section_title
        self.get_comments_template.get("json")["data"] = data
    
    def set_comment_preprocess_template(self, data):
        self.comments_preprocess_template.get("json")["data"] = data

    def set_summary_analysis_template(self, product_type_id, data):
        self.summary_analysis_template.get("json")["productTypeId"] = product_type_id
        self.summary_analysis_template.get("json").get("reviewsSummaryChart").get("data")["total"] = data.get("rating_total")
        self.summary_analysis_template.get("json").get("reviewsSummaryChart").get("data")["count"] = data.get("rating_count")
        self.summary_analysis_template.get("json").get("commentTypesSummaryChart").get("data")["total"] = data.get("total")
        self.summary_analysis_template.get("json").get("commentTypesSummaryChart").get("data")["count"] = [data.get("gib"), data.get("other")]
        self.summary_analysis_template.get("json")["data"] = data.get("return_data")

    def set_summary_sentiment_template(self, product_type_id, data):
        labels = list(map(lambda r: r.get("name"), aspect_definition.get(product_type_id).get("aspect")))
        self.summary_sentiment_template.get("json")["productTypeId"] = product_type_id
        self.summary_sentiment_template.get("json").get("stackedBarChart").get("data").get("datasets")[0]["data"] = data.get("positive")
        self.summary_sentiment_template.get("json").get("stackedBarChart").get("data").get("datasets")[1]["data"] = data.get("neutral")
        self.summary_sentiment_template.get("json").get("stackedBarChart").get("data").get("datasets")[2]["data"] = data.get("negative")
        self.summary_sentiment_template.get("json").get("stackedBarChart").get("data")["labels"] = labels
        self.summary_sentiment_template.get("json").get("stackedBarChart").get("data")["aspects"] = aspect_definition.get(product_type_id).get("aspect")

    def load(self):
        self._load_failure_json_template()
        self._load_aspect_definition_template()
        self._load_get_comments_template()
        self._load_comments_preprocess_template()
        self._load_summary_analysis_template()
        self._load_summary_sentiment_template()
        self._load_get_sentiment_template()
