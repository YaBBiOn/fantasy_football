"""데이터베이스 구성"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 연결하려는 db의 상대경로
SQLALCHEMY_DATABASE_URL = "sqlite:///./fantasy_data.db"

# db와 통신하는 통로(=연결 관리자) 생성.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread" : False}
)

# engine(db와의 연결을 돕는 관리자)를 사용해 작업하는 세션 생성
# 해당 세션을 기반으로 db와 실질적인 소통 가능
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# model.py내 class들(table)이 상속받을 부모 클래스. 
Base = declarative_base()