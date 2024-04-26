import json
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow

# إعداد تطبيق Flask
app = Flask(__name__)

# إعداد محرك قاعدة البيانات
engine = create_engine('sqlite:///database.db', echo=True)

# إعداد نموذج الجدول
Base = declarative_base()

class PersonalInfo(Base):
    __tablename__ = 'personal_info'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    profession = Column(String)
    skills = Column(String)

# إنشاء الجدول إذا لم يكن موجودًا بالفعل
Base.metadata.create_all(engine)

# إعداد جلسة
Session = sessionmaker(bind=engine)
session = Session()

# إعداد Marshmallow
ma = Marshmallow(app)

class PersonalInfoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'profession', 'skills')

personal_info_schema = PersonalInfoSchema(many=True)

# تعريف طرق الـ API
@app.route('/api/personal_info', methods=['GET'])
def get_personal_info():
    all_info = session.query(PersonalInfo).all()
    result = personal_info_schema.dump(all_info)
    return jsonify(result)

@app.route('/api/personal_info', methods=['POST'])
def update_personal_info():
    data = request.json
    new_info = PersonalInfo(name=data['name'], age=data['age'], profession=data['profession'], skills=json.dumps(data['skills']))
    session.add(new_info)
    session.commit()
    return jsonify({"message": "Personal info added successfully"})

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
