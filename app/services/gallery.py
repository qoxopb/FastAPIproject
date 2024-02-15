import os
from datetime import datetime

import requests
from sqlalchemy import insert, select, update, func, or_
from app.dbfactory import Session
from app.models.gallery import Gallery, GalAttach

# 이미지파일 저장경로 설정
UPLOAD_DIR = 'C:/Java/nginx-1.25.3/html/cdn'


class GalleryService:
    @staticmethod
    def gallery_convert(gdto):
        data = gdto.model_dump()
        # data.pop('response')   # captcha 확인용 변수 response는 제거
        gal = Gallery(**data)
        data = {'userid': gal.userid, 'title': gal.title,
                'contents': gal.contents}
        return data


    @staticmethod
    def insert_gallery(gdto, fname, fsize):
        data = GalleryService.gallery_convert(gdto)
        with Session() as sess:
            stmt = insert(Gallery).values(data)
            result = sess.execute(stmt)
            sess.commit()

            data = {'fname': fname, 'fsize': fsize, 'gno': result.inserted_primary_key[0]}
            print(result.inserted_primary_key)
            stmt = insert(GalAttach).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result


    @staticmethod
    async def process_upload(attach):
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        nfname = f'{today}{attach.filename}'    #파일명
        fsize = attach.size                     #파일크기
        # os.path.join(A,B) =>A/B   (경로 생성)
        fname = os.path.join(UPLOAD_DIR, nfname)

        #비동기 처리를 위해 함수에 await 지시자 추가
        # 이 경우 함수 정의부분에 async 지시자 추가 필요.
        content = await attach.read()   #업로드한 파일의 내용을 비동기로 모두 읽어옴

        with open(fname, 'wb') as f:
            f.write(content)        # 파일 내용을 저장한 파일이름으로 저장

        return nfname, fsize





    @staticmethod
    def select_gallery(cpg):
        stnum = (cpg - 1) * 25
        with Session() as sess:
            cnt = sess.query(func.count(Gallery.gno)).scalar() # 총게시글수

            stmt = select(Gallery.gno, Gallery.title, Gallery.userid,
                          Gallery.regdate, Gallery.views, GalAttach.fname)\
            .join_from(Gallery, GalAttach)\
            .order_by(Gallery.gno.desc()).offset(stnum).limit(25)
            result = sess.execute(stmt)

        return result, cnt


    # @staticmethod
    # def find_select_board(ftype, fkey, cpg):
    #     stnum = (cpg - 1) * 25
    #     with (Session() as sess):
    #         stmt = select(Board.bno, Board.title, Board.userid,
    #                       Board.regdate, Board.views)
    #
    #         # 동적 쿼리 작성 - 조건에 따라 where절이 바뀜
    #         myfilter = Board.title.like(fkey)
    #         if ftype == 'userid': myfilter = Board.userid.like(fkey)
    #         elif ftype == 'contents': myfilter = Board.contents.like(fkey)
    #         elif ftype == 'titconts': myfilter = \
    #                   or_(Board.title.like(fkey), Board.contents.like(fkey))
    #
    #         stmt = stmt.filter(myfilter)\
    #             .order_by(Board.bno.desc()).offset(stnum).limit(25)
    #         result = sess.execute(stmt)
    #
    #         cnt = sess.query(func.count(Board.bno))\
    #             .filter(myfilter).scalar() # 총게시글수
    #
    #     return result, cnt
    #
    #
    # @staticmethod
    # def selectone_board(bno):
    #     with Session() as sess:
    #         stmt = select(Board).filter_by(bno=bno)
    #         result = sess.execute(stmt).first()
    #
    #     return result
    #
    #
    # @staticmethod
    # def update_count_board(bno):
    #     with Session() as sess:
    #         stmt = update(Board).filter_by(bno=bno)\
    #             .values(views=Board.views+1)
    #         result = sess.execute(stmt)
    #         sess.commit()
    #
    #     return result
    #
    # # google recaptcha 확인 url
    # # https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
    # @staticmethod
    # def check_captcha(bdto):
    #     data = bdto.model_dump()  # 클라이언트가 보낸 객체를 dict로 변환
    #     req_url = 'https://www.google.com/recaptcha/api/siteverify'
    #     params = { 'secret': '',
    #                'response': data['response'] }
    #     res = requests.get(req_url, params=params)
    #     result = res.json()
    #     # print('check', result)
    #
    #     # return result['success']
    #     return True

