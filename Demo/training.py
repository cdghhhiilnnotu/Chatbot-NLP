import random
import json
import pickle
import numpy as np
import nltk
from keras.optimizers import SGD
from keras.models import Sequential
from keras.layers import Dense, Dropout
nltk.download('punkt')

# Load, đọc file json lưu vào intents
intents = json.loads(open('intents.json').read())

# List chứa tất cả các từ trong kịch bản intents
words = []
# List chứa các tag trong intents
classes = []
# List chứa các tuple (các từ, tag) của mỗi intent
documents = []
# List chứa các dấu câu không cần thiết
ignore_letters = ['?', '!', '.', ',']

# Lặp qua các phần tử trong list giá trị của key 'intents'
for intent in intents['intents']:
    # Lặp qua các phần tử trong list giá trị của key 'patterns'
    for pattern in intent['patterns']:
        # Tách 1 câu thành các từ cho vào 1 list
        word_list = nltk.word_tokenize(pattern)
        # Nối các từ vừa được tách vào list words
        words.extend(word_list)
        # Thêm tuple(list các từ, tag) vào list documents
        documents.append((word_list, intent['tag']))
        # Thêm tag vào list classes nếu classes chưa có tag đó
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Chuyển các chữ hoa thành chữ thường, loại bỏ các dấu câu
words = [word.lower() for word in words if word not in ignore_letters]
# Loại bỏ các từ trùng nhau, sắp xếp các từ trong list word
words = sorted(set(words))
# Loại bỏ các từ trùng nhau, sắp xếp các từ trong list classes
classes = sorted(set(classes))
# Tạo(nếu chưa có) và mở file words.pkl và viết list words vào file
pickle.dump(words, open('words.pkl', 'wb'))
# Tạo(nếu chưa có) và mở file classes.pkl và viết list classes vào file
pickle.dump(classes, open('classes.pkl', 'wb'))

# Tạo list training chứa
# tuple(các dãy giá trị của 1 câu, giá trị của tag cho câu đó)
training = []

# Lọc qua các tuple trong list documents
for doc in documents:
    # Tạo list bag chứa giá trị khi đối chiếu phần tử trong list words với word_pattern
    # Đối chiếu các từ đó vào list word_pattern và biển diễn sự tồn tại của từ đấy bằng giá trị 1 0
    bag = []
    # Tạo list chứa các list từ của 1 câu trong intents
    word_patterns = doc[0]
    # Chuyển chữ hoa thành chữ thường và loại bỏ dấu câu
    word_patterns = [word.lower() for word in word_patterns if word not in ignore_letters]

    # Chạy qua các phần tử của list words
    for word in words:
        # Nếu phần tử word trong list words có xuất hiện trong list word_pattern
        # Thêm giá trị 1 vào list bag, nếu ko thêm giá trị 0
        bag.append(1) if word in word_patterns else bag.append(0)

    # Tạo list output_row bằng độ dài list classes,
    # để biểu diễn giá tag của câu đang xử lí
    output_row = [0] * len(classes)
    # Thay đổi giá trị tương ứng với tag trong classes thành 1
    output_row[classes.index(doc[1])] = 1
    # Thêm tuple(giá trị các từ trong 1 câu, tag tương ứng với dãy giá trị đó)
    training.append([bag, output_row])

# Trộn list training
random.shuffle(training)
# Chuyển các list con trong list training sang dạng numpy để xử lí list,có kiểu dữ liệu object
# Do chứa 2 mạng ko đều nhau
training = np.array(training, dtype=object)

# Tạo list train_x chứa giá trị training đầu vào
# Lấy các phần tử 0 của list training (Các dãy giá trị của 1 câu)
train_x = list(training[:,0])
# Tạo list train_y chứa giá trị training đầu ra
# Lấy các phần tử 1 của list training (Các dãy giá trị của 1 tag)
train_y = list(training[:,1])

# Tạo model kiểu keras.Sequential
model = Sequential()

# Tạo mạng thần kinh neural network cho model để training
# Đầu vào là số lượng các phần tử của train_x[0] = độ dài list words
# Đầu ra là số lượng các phần tử của train_y[0] = độ dài list classes
model.add(Dense(120, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(60, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Tạo thông số nâng cấp khả năng học, giảm sự sai sót cho model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Bắt đầu training model và lưu, xuất model vào file chatbot_model.h5
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
# Thông báo hoàn thành training
print('Done')
