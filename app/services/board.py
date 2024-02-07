from sqlalchemy import insert

from app.dbfactory import Session
from app.models.board import Board



class BoardService():
    @staticmethod
    def board_convert(bdto):
        data = bdto.model_dump()
        bd = Board(**data)
        data = {'userid':bd.userid, 'title':bd.title, 'contents':bd.contents}
        return data


    @staticmethod
    def insert_board(bdto):
        # 변환된 회원정보를 member 테이블에 저장
        data = BoardService.board_convert(bdto)
        with Session() as sess:
            stmt = insert(Board).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result


