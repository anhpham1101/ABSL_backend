PHONE = {
    "sound": "Âm thanh",
    "screen": "Màn hình",
    "camera": "Camera",
    "feature": "Tính năng",
    "battery": "Pin",
    "perfomance": "Cấu hình - Hiệu năng",
    "design": "Thiết kế",
    "price": "Giá",
    "accessory": "Phụ kiện",
    "general": "Chung chung của sản phẩm",
    "shipping": "Giao hàng",
    "packaging": "Đóng gói",
    "consulting": "Tư vấn",
    "service-general": "Dịch vụ chung chung"
}

CLOTH = {
    "bo-phan-ao": "Bộ phận áo",
    "chat-lieu": "Chất liệu",
    "chung-chung": "Chung chung của sản phẩm",
    "consulting": "Tư vấn",
    "gia-ca": "Giá cả",
    "mau-sac": "Màu sắc",
    "packaging": "Đóng gói",
    "service-general": "Chung chung của dịch vụ",
    "shipping": "Giao hàng",
    "thiet-ke-kich-thuoc": "Thiết kế - Kích thước",
    "tinh-trang-ao": "Tình trạng áo"
}

SENTIMENT = {
    1: "rgb(66, 245, 75)",
    2: "rgb(255, 232, 105)",
    3: "rgb(255, 70, 70)"
}

OTHER = {
    1: "rgb(125, 125, 125)"
}

class TransformValue:
    def __init__(self, comment_ids, comment_sentiments, product_id):
        self.product_id = product_id
        self.comments = zip(comment_ids, comment_sentiments)
        self.mapping = CLOTH if product_id == 1 else PHONE
        self.transformed_data = []

    def transform(self):
        for comment_id, comment_sentiment in self.comments:
            tagInfos = []
            for key, value in comment_sentiment.items():
                if key == 'other' and value != 0:
                    tagInfos.append({
                        'content': "Nhận xu",
                        'textColor': OTHER.get(1)
                    })
                elif value != 0:
                    tagInfos.append({
                        'content': self.mapping.get(key),
                        'textColor': SENTIMENT.get(value)
                    })
            self.transformed_data.append({
                'commentId': comment_id,
                'tagInfos': tagInfos
            })
        return self.transformed_data
