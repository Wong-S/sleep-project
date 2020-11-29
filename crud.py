"""CRUD operations"""
from datetime import datetime, time

import YouTube

# FIXME NOTE: Since taking things from model, would be best to import all from model?
# NOTE: CRUD -> create, read, update, delete
from model import (
    db,
    User,
    Journal,
    SleepLog,
    Playlist,
    Video,
    Category,
    VideoCategories,
    connect_to_db,
)

# =================================================================
# CREATE USER TABLE, link to Model.py
# NOTE: 'first_name' must be same as called in model.py Class
# Part 1: Create user
def create_user(first_name, last_name, email, password, timezone):
    """Create and return a new user"""

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        timezone=timezone,
    )

    db.session.add(user)
    db.session.commit()

    return user


# NOTE --> Email and Password are Unique!
# Test run in interactive mode:
# create_user('F','L', 'test@.com','124')


# NOTE: CHECKING functions display user emails that were added!

# =================================================================
# USER SECTION:
# Server.py create account POST function
def get_user():
    """Return list of user objects"""

    return User.query.all()


# NOTE: Getting list of objects from class User

# NOTE: Test interactively returns list of user objects


def get_user_by_id(user_id):
    """Return user's profile with user's email"""

    user_by_id = User.query.get(user_id)

    return user_by_id


# NOTE: This returns at that specific id key for that user, with their info like name, email, etc. That you can make an instance attribute, etc
# <User user_id 1 first_name = David >


def get_user_by_email(email):
    """ Return user's profile or None """

    return User.query.filter(User.email == email).first()


# Server.py login route:
def check_password(email, password):
    """ Compare password on file for a user when they are logging in"""

    user_info = get_user_by_email(email)

    if user_info == None:
        return False
    elif user_info.password == password:
        return True
    else:
        return False


# ================================================================
# JOURNAL SECTION:

# Part 2:
# Create a Journal entry for user:
def create_journal_entry(
    user_id,
    entry_name,
    entry_details,
    created_at,
    updated_at
    # created_at=datetime.now(),
    # updated_at=datetime.now(),
):
    """Create and return a new journal entry"""

    journal = Journal(
        user_id=user_id,
        entry_name=entry_name,
        entry_details=entry_details,
        created_at=created_at,
        updated_at=updated_at
        # created_at=datetime.date(created_at),
        # updated_at=datetime.date(updated_at),
        # NOTE: Foreign Key from User Table
    )

    db.session.add(journal)
    db.session.commit()

    return journal


# NOTE --> Need datetime.now() for when the exact moment created_at and updated_at occur. Might need to revise created_at to be fixed.
# Test run in interactive mode:
# 1) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove', '31-Oct-2020', '31-Oct-2020')
# OR:
# 2) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove', '31-Oct-2020', None)
# OR:
# 3) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove', '31-Oct-2020')
# OR:
# 4) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove')


def get_user_journal(user_id):
    """Return journal list of objects if email matches"""

    user_by_id = User.query.get(user_id)
    return Journal.query.all()


def check_user_to_journal_id(user_id):
    """Return joinedload user objects joined with journal table"""

    # user_id = int(user_id)
    return (
        User.query.filter(User.user_id == user_id)
        .options(db.joinedload("journals"))
        .first()
    )


# ================================================================
# PLAYLIST--VIDEO SECTION:
# Part 3:

# Create a Video Category (ie: rain, fan, ocean, etc.)
def create_category(category_name):
    """Create and return a new category"""

    category = Category(category_name=category_name)

    db.session.add(category)
    db.session.commit(category)

    return category


# NOTE: Not really sure how this table works exactly. Would I still need to seed in database or can query?
# Create a Video and Categories
def create_video_categories(video_id, category_id):
    """Create and return a new video with category id associated"""

    video_category = VideoCategories(video_id=video_id, category_id=category_id)

    db.session.add(video_category)
    db.session.commit(video_category)

    return video_category


# Create a Playlist
def create_playlist(playlist_name, user_id):
    """Create and return a new playlist"""

    playlist = Playlist(playlist_name=playlist_name, user_id=user_id)

    db.session.add(playlist)
    db.session.commit()

    return playlist


######################################################################

# Create a Video

# NOTE FIXME: The very first playlist user creates will default to value of id of 1. After that, should increment with each new one???
def create_video(video_title, video_duration, video_url, playlist_id):
    """Create and return a new video to a playlist
    
    >>>create_video('The rain falls', 'medium', 'X6SF3f2')
    """

    video = Video(
        video_title=video_title,
        # description=description,
        video_duration=video_duration,
        video_url=video_url,
        playlist_id=playlist_id,
    )

    db.session.add(video)
    db.session.commit()

    return video


######################################################################

# Create Duration for each video
# FIXME: May not need this added as another table in the database

# def create_video_duration(video_id, duration_length):
#     """Create and return the video's duration"""

#     video_duration = VideoDuration(video_id=video_id, duration_length=duration_length)

#     db.session.add(video_duration)
#     db.session.commit()

#     return video_duration


######################################################################
# NOTE:Where YouTube.py functions come are implemented. TODO:Check if correct Doctests below?


def display_selected_videos(video_category, video_duration):
    """Return list of selected video attributes
    
    >>> display_selected_videos("rain sounds", "long")
    [('Relaxing Sleep Music + Rain Sounds - Relaxing Music, Insomnia, Stress Relief Music', 'OSF7W68CKmE'), ('Thunder and Rain Sounds WHITE SCREEN for Sleep &amp; Relaxation | White Screen Rain Sounds', 'OEqgFkFBrlk'), ('🎧 Thunder &amp; Rain Sounds By Treehouse | Go to Sleep with Ambient Noise, @Ultizzz day#66', '1NwacRwhMug'), ('Heavy Thunderstorm w/ Rain Sounds - Thunder &amp; Lightning Rain on Window for Sleeping, Study and Relax', 'qMi2z2m3bsM'), ('Rain Sounds + Peaceful Piano - Relaxing Sleep Music, Insomnia, Meditation Music', 'JbGKtO47Jp8')]

    """

    selected_video = YouTube.search_videos(video_category, video_duration)
    # print(selected_video)   #NOTE:Print list with tuples

    return selected_video


def check_user_to_playlist_id(user_id):
    """Return joinedload user objects joined with playlists table"""

    # user_id = int(user_id)
    return (
        User.query.filter(User.user_id == user_id)
        .options(db.joinedload("playlists"))
        .first()
    )


def get_videos_from_playlist_id(playlist_id):
    """Return joinedload video objects joined with playlists table"""

    # user_id = int(user_id)
    return (
        Playlist.query.filter(Playlist.playlist_id == playlist_id)
        .options(db.joinedload("videos"))
        .first()
    )


# ================================================================
# SLEEP LOG SECTION
# Part 4:

# Create a Sleep Log entry for user: FIXME: variable fix
def create_sleep_log(user_id, wake_time, bed_time, current_date):
    """Create and return a new sleep log entry"""

    sleep_log = SleepLog(
        user_id=user_id,
        wake_time=wake_time,
        bed_time=bed_time,
        current_date=current_date,
    )
    # bed_time=bed_time.strftime("%H:%M")
    db.session.add(sleep_log)
    db.session.commit()

    return sleep_log


# NOTE: Run in interactive terminal test:
# create_sleep_log(user_id = 7, wake_time = 23:11:00, bed_time = 18:28:00, current_date = 2020-11-15)
# <SleepLog sleep_log_id = 1 wake_time = 23:11:00 bed_time = 18:28:00 current_date = 2020-11-15>
# >>> u = create_sleep_log(1, '23:11:00', '18:28:00', '2020-11-15')
# create_sleep_log(1, time(7, 46, 00), time(22, 46, 00), '2020-11-15')


def get_sleep_data_user_id(user_id):
    """Return joinedload user objects joined with sleep_logs table"""

    # user_id = int(user_id)
    return (
        User.query.filter(User.user_id == user_id)
        .options(db.joinedload("sleep_logs"))
        .first()
    )


def get_sleep_data_by_date(user_id, current_date_lst, correct_date_obj):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)
    # // TODO THIS IS WRONG! I NEED TO PASS IN THE DATE THE USER CLICKS....
    for date in user_id_sleep_log_obj.sleep_logs:
        if correct_date_obj in current_date_lst:
            print("IS THIS THE RIGHT DATE?", correct_date_obj)
            return SleepLog.query.filter(
                SleepLog.current_date == correct_date_obj
            ).first()

    # user_id = int(user_id)
    # return SleepLog.query.filter(SleepLog.current_date == date).first()


def get_sleep_data_by_filtered_date(user_id, chosen_date_by_user):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)

    print("HEY IS IT WORKING??")

    for date in user_id_sleep_log_obj.sleep_logs:
        if chosen_date_by_user == date.current_date:
            print("THIS IS THE DATE YOU FILTERED OUT?", date.current_date)
            return SleepLog.query.filter(
                SleepLog.current_date == chosen_date_by_user
            ).first()


def get_sleep_time_by_filtered_date_lst(user_id, date_obj_lst):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)

    print("HEY IS IT WORKING??")
    # FIXME: REMOVE LATER! JUST FOR CHECKING
    # print(date_obj_lst)
    # for i in date_obj_lst:
    #     print(i)
    #     for x in i:
    #         print("THE DATE OBJECT IS?:", x)

    selected_date_obj_lst = []
    for all_dates in user_id_sleep_log_obj.sleep_logs:
        print(all_dates.current_date)
        print(type(all_dates.current_date))
        for (
            date_lst
        ) in (
            date_obj_lst
        ):  # Need a nested loop since date_obj_lst is a session so a list within another list
            for date_obj in date_lst:
                print(date_obj)
                print(type(date_obj))
                if date_obj == all_dates.current_date:
                    print("THIS IS THE DATE YOU FILTERED OUT?", all_dates.current_date)
                    query_obj = SleepLog.query.filter(
                        SleepLog.current_date == date_obj
                    ).first()

                    selected_date_obj_lst.append(query_obj)
    # NOTE: JUST FOR CHECKING! IT WORKS
    print(selected_date_obj_lst)
    return selected_date_obj_lst


def get_sleep_time_by_filtered_month_lst(user_id, month_date_obj_lst):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)

    print("HEY IS IT WORKING??")
    # FIXME: REMOVE LATER! JUST FOR CHECKING
    # print(date_obj_lst)
    # for i in date_obj_lst:
    #     print(i)
    #     for x in i:
    #         print("THE DATE OBJECT IS?:", x)

    selected_date_obj_lst = []
    for all_dates in user_id_sleep_log_obj.sleep_logs:
        print("FIRST PART:", all_dates.current_date)
        print(type(all_dates.current_date))
        for date_in_lst in month_date_obj_lst:
            print("SECOND PART WORKING!?:", date_in_lst)
            print(type(date_in_lst))
            if all_dates.current_date == date_in_lst:

                print("THIS IS THE DATE YOU FILTERED OUT?", all_dates.current_date)
                print("????", month_date_obj_lst)
                query_obj = SleepLog.query.filter(
                    SleepLog.current_date == all_dates.current_date
                ).first()

                selected_date_obj_lst.append(query_obj)
    # NOTE: JUST FOR CHECKING! IT WORKS
    print(selected_date_obj_lst)
    return selected_date_obj_lst


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
