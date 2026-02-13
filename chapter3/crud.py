"""sqlalchemy 쿼리 함수"""

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date
import models

def get_player(db:Session,
               player_id:int) :
    '''
    주어진 player_id에 해당하는 Player 레코드를 조회하는 함수
    '''
    return db.query(models.Player).filter(
        models.Player.player_id == player_id).first()


def get_players(db:Session,
                skip:int = 0,
                limit:int = 100,
                min_last_changed_date: date= None,
                last_name: str=None,
                first_name: str=None):
    '''
    주어진 조건(날짜, 성, 이름)에 해당되는 Player 레코드를 조회하는 함수
    skip : 위에서 일정 개수만큼은 생략함. 기본값은 0
    limit : 최대치로 보여주는 레코드 개수. 기본값은 100
    min_last_changed_date : 데이터 갱신 날짜. 기본값 X
    last_name : player의 성. 기본값 X
    first_name : player의 이름. 기본값 X
    '''
    query = db.query(models.Player)
    if min_last_changed_date:
        qurey = query.filter(
            models.Player.last_changed_date >= min_last_changed_date
        )
    if first_name:
        query = query.filter(
            models.Player.first_name == first_name
        )
    if last_name:
        query = query.filter(
            models.Player.last_name == last_name
        )
    return query.offset(skip).limit(limit).all()

def get_league(db: Session,
               league_id: int = None):
    '''
    league_id에 맞는 리그를 League 레코드에서 조회하는 함수
    '''
    return db.query(models.League).filter(
        models.League.leauge_id == league_id).first()

def get_leagues(db: Session,
                skip: int = 0,
                limit: int = 100,
                min_last_changed_date: date = None,
                league_name: str = None):
    '''
    주어진 조건(날짜, 리그명)에 해당되는 리그명을
    조인된 League 레코드에서 조회하는 함수
    skip : 위에서 일정 개수만큼은 생략함. 기본값은 0
    limit : 최대치로 보여주는 레코드 개수. 기본값은 100
    min_last_changed_date : 데이터 갱신 날짜. 기본값 X
    league_name : 리그명
    '''
    # League가 Player 랑 M:N관계이기 때문에 joinload를 통해 한번에 League.team에 접근함
    # 단, 리그랑 팀이 너무 많아지면 row가 중복해서 느려질 수 있음
    # 그럴 때에는 selectinload를 통해 리그를 먼저 가지고 오고 in 으로 팀을 가지고 와서 합치자
    query = db.query(models.League).options(joinedload(models.League.teams))
    if min_last_changed_date:
        query = query.filter(
            models.League.last_changed_date > min_last_changed_date
        )
    if league_name:
        query = query.filter(models.League.league_name == league_name)
    return query.offset(skip).limit(limit).all()

def get_teams(db: Session,
              skip: int = 0,
              limit: int = 100,
              min_last_changed_date: date = None,
              team_name: str = None,
              league_id: int = None):
    '''
    주어진 조건(날짜, 팀이름, 리그 야이디)에 해당되는 Team 레코드를 조회하는 함수
    skip : 위에서 일정 개수만큼은 생략함. 기본값은 0
    limit : 최대치로 보여주는 레코드 개수. 기본값은 100
    min_last_changed_date : 데이터 갱신 날짜. 기본값 X
    team_name : 팀 이름. 기본값 X
    league_id : 리그에 있는 id. 기본값 X
    '''
    query = db.query(models.Team)
    if min_last_changed_date:
        query = query.filter(models.Team.last_changed_date >= min_last_changed_date)
    if team_name:
        query = query.filter(models.Team.team_name == team_name)
    if league_id:
        query = query.filter(models.Team.league_id == league_id)
    return query.offset(skip).limit(limit).all()

# 분석 쿼리
def get_player_count(db: Session):
    '''
    Player에 있는 선수 수를 카운트하는 함수
    '''
    query = db.query(models.Player)
    return query.count()

def get_team_count(db: Session):
    '''
    Team에 있는 팀 수를 카운트하는 함수
    '''
    query = db.query(models.Team)
    return query.count()

def get_league_count(db: Session):
    '''
    League에 있는 리그 수를 카운트하는 함수
    '''
    query = db.query(models.League)
    return query.count()
