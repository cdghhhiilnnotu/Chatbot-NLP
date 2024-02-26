import random
import json
import pickle
import numpy as np
import nltk
from keras.models import load_model

# Load, đọc file json lưu vào intents
intents = json.loads(open('intents.json').read())
# Load, đọc file 'words.pkl' lưu vào list words
words = pickle.load(open('words.pkl', 'rb'))
# Load, đọc file 'classes.pkl' lưu vào list classes
classes = pickle.load(open('classes.pkl', 'rb'))
# Load, đọc file chatbot_model.h5 lưu vào đối tượng model
model = load_model('chatbot_model.h5')
# List chứa các dấu câu không cần thiết
ignore_letters = ['?', '!', '.', ',']


# Hàm tách từ, loại bỏ dấu trong 1 câu
# Và trả về list chứa các từ đó
def clean_up_sentence(sentence):
    # Tách 1 câu thành các từ cho vào 1 list sentence_words
    sentence_words = nltk.word_tokenize(sentence)
    # Chuyển các chữ hoa thành chữ thường, loại bỏ các dấu câu
    sentence_words = [w.lower() for w in sentence_words if w not in ignore_letters]
    # Trả về list chứa các từ trong câu
    return sentence_words


# Hàm chuyển đổi giá trị cho model
# Hàm sẽ nhận vào 1 câu và chuyển thành 1 list các từ
# Đối chiếu các từ đó vào list words và biển diễn sự tồn tại của từ đấy bằng giá trị 1 0
def bag_of_words(sentence):
    # Chuyển câu thành list các từ
    sentence_words = clean_up_sentence(sentence)
    # Tạo list biểu diễn các từ trong list sentence_words
    # Khi chiếu lên words
    bag = [0] * len(words)
    # Chạy qua các phần tử của list sentence_words
    for w in sentence_words:
        # Chạy qua các phần tử của list words và đếm số thứ tự
        for i, word in enumerate(words):
            # Nếu w (trong sentence_words) = word (trong words)
            # Thì gán giá trị vị trí i của list bag = 1
            if word == w:
                bag[i] = 1
    # Trả về biểu diễn nhị phân của các từ theo list words
    return np.array(bag)


# Dự đoán thể loại của 1 câu
def predict_class(sentence):
    # Tạo list biểu diễn nhị phân của các từ theo list words
    bow = bag_of_words(sentence)
    print(bow)
    # Gọi hàm predict của lớp Sequential để tính các xác suất cho thể loại
    # Gán list giá trị xác suất vào list res
    res = model.predict(np.array([bow]))[0]
    print(f'Res: {res}')
    # Đánh số thứ tự các xác suất theo vị trí của các tag trong classes
    # Và gán vào list result
    result = [[i, r] for i, r in enumerate(res)]
    print(result)
    # Sắp xếp list result theo thứ tự xác suất từ cao đến thấp
    result.sort(key=lambda x: x[1], reverse=True)
    # Tạo list trả về các trường hợp câu trả lời
    return_list = []
    # Chạy qua các phần tử của list result
    # Và thêm tên tag, xác suất của tag đó
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    print(return_list)
    # Trả về các câu trả lời
    return return_list


# Thuật toán tìm kiêm tuần tự
# Xem xét kết quả dự đoán ý nghĩa câu hỏi >= 75% thì đưa ra câu trả lời trong kịch bản
def sequential_search(tag, lst, prob):
    if prob >= 0.75:
        for i in lst:
            if i['tag'] == tag:
                return random.choice(i['responses'])
    return 'Sorry i can\'t undertand'


# Hàm tính toán xác suất các câu trả lời
# Và trả về câu trả lời có xác suất lớn nhất
def get_response(msg):
    # Tính toán xác xuất theo câu hỏi nhận vào
    ints = predict_class(msg)
    # Gán giá trị tag
    tag = ints[0]['intent']
    # Tạo list các intent trong kịch bản
    list_of_intents = intents['intents']

    # Trả về câu trả lời theo thuật toán tìm kiếm tuần tự
    return sequential_search(tag,list_of_intents,float(ints[0]['probability']))


# Thông báo chat bot sẵn sàng trả lời câu hỏi
print('BOT is ready')
