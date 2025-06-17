from typing import Dict, Any, List
from utils.db_ctx import get_db
from utils.sql_loader import load_sql

def init_database():

    init_schema = load_sql('init_schema.sql')
    print('LOADING DATABASE')
    with get_db() as conn:
        
        cursor = conn.cursor()
        cursor.executescript(init_schema)
        conn.commit()

def get_guild_settings(guild_id):

    ggs_script = load_sql('get_guild_settings.sql', 'queries')

    with get_db() as conn:

        cursor = conn.cursor()
        cursor.execute(ggs_script, {'guild_id': guild_id})

        guild_settings = cursor.fetchone()

        if not guild_settings:

            ang_sql = load_sql('add_new_guild.sql', 'inserts')
            cursor.execute(ang_sql, {'guild_id': guild_id})
            conn.commit()

            cursor.execute(ggs_script, {'guild_id': guild_id})
            guild_settings = cursor.fetchone()

        
        
    return dict(guild_settings)

def configure_guild_settings(guild_id, updated_settings: Dict[str, Any]):

    ugs_script = load_sql('update_guild_settings.sql', 'inserts')

    update_clause = ', '.join([f"{key} = :{key}" for key in updated_settings])
    ugs_script = ugs_script.format(update_clause=update_clause)
    
    updated_settings['guild_id'] = guild_id

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(ugs_script, updated_settings)
        conn.commit()
    
    return

def save_infraction(infraction: Dict[str, Any]):
    si_script = load_sql('save_infraction.sql', 'inserts')

    with get_db() as conn:

        cursor = conn.cursor()
        cursor.execute(si_script, infraction)

        conn.commit()
    
    return

def get_infraction_by_message(message_id) -> Dict[str, Any]:
    gibm_script = load_sql('get_infraction_by_message.sql', 'queries')

    with get_db() as conn:

        cursor = conn.cursor()
        cursor.execute(gibm_script, {'message_id': message_id})
        infraction = cursor.fetchone()
    
    if infraction:
        return dict(infraction)
    else:
        return None

def update_infraction_votes(infraction_id, approve_votes, reject_votes):

    uiv_sql = load_sql('update_infraction_votes.sql', 'inserts')

    votes_data = {
        'infraction_id': infraction_id,
        'approve_votes': approve_votes,
        'reject_votes': reject_votes,
    }

    with get_db() as conn:

        cursor = conn.cursor()
        cursor.execute(uiv_sql, votes_data)
        conn.commit()

    return

def finalize_infraction(infraction_id, status, approve_votes, reject_votes):

    fi_sql = load_sql('finalize_infraction.sql', 'inserts')

    finalize_data = {
        'id': infraction_id,
        'status': status,
        'approve_votes': approve_votes,
        'reject_votes': reject_votes
    }

    with get_db() as conn:
        
        cursor = conn.cursor()
        cursor.execute(fi_sql, finalize_data)
        conn.commit()
    
    return

def get_user_infractions(guild_id, user_id) -> Dict[str, Any]:

    gui_scripts = load_sql('get_user_infractions.sql', 'queries')
    
    id_dict = {
        'guild_id': guild_id,
        'user_id': user_id,
    }

    with get_db() as conn:

        cursor = conn.cursor()
        cursor.execute(gui_scripts, id_dict)

        user_infractions = cursor.fetchall()
    
    return [dict(row) for row in user_infractions]


def get_guild_leaderboard(guild_id, limit=3) -> List[Dict[str, Any]]:
    print('in database func for guild_leaderboard')
    ggl_script = load_sql('get_guild_leaderboard.sql', 'queries')

    ggl_data = {
        'guild_id': guild_id,
        'limit': limit,
    }

    with get_db() as conn:

        cursor = conn.cursor()
        cursor.execute(ggl_script, ggl_data)
        infraction_leaderboard = cursor.fetchall()
    
    return [dict(user_stats) for user_stats in infraction_leaderboard]


def get_pending_infractions(guild_id) -> List[Dict[str, Any]]:

    gpi_script = load_sql('get_pending_infractions.sql', 'queries')

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(gpi_script, {'guild_id': guild_id})
        pending_infractions = cursor.fetchall()


    return [dict(pending_infraction) for pending_infraction in pending_infractions]


def get_all_pending_infractions() -> List[Dict[str, Any]]:

    gapi_script = load_sql('get_all_pending_infractions.sql', 'queries')

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(gapi_script)
        all_pending_infractions = cursor.fetchall()
    
    return [dict(pending_infraction) for pending_infraction in all_pending_infractions]


def clear_pending_infractions() -> None:

    cpi_script = load_sql('clear_pending_infractions.sql', 'deletes')

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(cpi_script)
    
    return




