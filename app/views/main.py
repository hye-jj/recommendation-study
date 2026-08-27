from flask import Blueprint, render_template, url_for, redirect
from flask import request
from .etc import sub
import pandas as pd
import numpy as np


bp = Blueprint('main', __name__, url_prefix='/')

user_rfm = pd.read_pickle('./data/user_rfm.pkl')
item_rfm = pd.read_pickle('./data/item_rfm.pkl')
cus = pd.read_pickle('./data/cus.pkl')
rating = pd.read_pickle('./data/rating.pkl')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/', methods=["POST", "GET"])
def index():
    data_list = range(1,5)        
    title, content = 'Title', '상품을 추천해 볼까요'  
    # 추천 함수
    # 입력 : 사용자 
    #cus_id = int(2)  #  << 페이지에서 받아오기
    if request.method == 'POST':
        cus_id = int(request.form['num'])
        # 빈도군집, 나이군집
        fre_X, age_X = sub.data_read(cus_id, cus, rating)
        # 유사도
        fre_item_sim_df, fre_user_sim_df = sub.cal_similarity(fre_X)
        # age_item_sim_df, age_user_sim_df = cal_similarity(age_X)

        # 군집의 고객이 가장 많이 구매한 상품 30개중 랜덤 검색하여
        random_item = pd.DataFrame(fre_X.scls_c_nm.value_counts()[:30]).sample(n=1).index[0]

        cluster = cus[cus.cno == cus_id].fre_clu.values[0]

        top_item_li = sub.top_item(random_item, fre_item_sim_df)
        # top_users_li = sub.top_users(cus_id, fre_X, fre_user_sim_df)

        contents = { 'cus_id':cus_id, 'data_list': data_list, 'random_item': random_item, 
                'cluster': cluster, 'top_item_li': top_item_li}
        
        return render_template('index.html', contents=contents)
    
    else:
        cus_id = None
        contents = cus_id
    return render_template('index.html', contents=contents)