"""sqlalchemy 모델"""
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from database import Base

class Player(Base):
    __tablename__ = "player"

    player_id = Column(Integer, primary_key=True, index=True)
    gsis_id = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    Last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    # relationship(연결할 ORM클래스명, secondary=다대다 관계를 풀 때 참고할 중간 테이블의 문자열, back_population=반대편 ORM클래스 안에 정의된 relationship 속성명)
    performances = relationship("Performance", back_populates="player")

    teams = relationship("Team", secondary="Team_player", back_polulates="player")

class Performance(Base):
    __tablename__ = "performance"

    performance_id = Column(Integer, primary_key=True, index=True)
    week_number = Column(String, nullable=False)
    fantasy_points = Column(Float, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    # FK 작성. 관계형으로 되어있는데, FK에 대한 정의가 있는 경우, FK가 있는 테이블이 N에 속함
    player_id = Column(Integer, ForeignKey("player.player_id"))

    player = relationship("Player", back_populates="performances")

class Team(Base):
    __tablename__ = "team"

    league_id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date =Column(Date, nullable=False)

    teams = relationship("Team", back_populates="league")

class Team(Base):
    __tablename__ = "team"

    team_id = Column(Integer, primary_key=True, index=False)
    team_name = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    league_id = Column(Integer, ForeignKey("league.league_id"))
    league = relationship("League", back_populates="teams")
    players = relationship("Player", secondary="team_player", back_populates="teams")

class TeamPlayer(Base):
    __tablename__ = "teamplayer"

    team_id = Column(Integer, ForeignKey("team.team_id"), primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.player_id"), primary_key=True)
    last_changed_date = Column(Date, nullable=False)


