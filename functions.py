# functions.py
import bcrypt
from db import mydb

db_client = mydb()

def _hash_password(raw_password: str) -> bytes:

    return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())


def _check_password(raw_password: str, hashed_password: bytes) -> bool:
    """Check plaintext password against bcrypt hash."""
    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed_password)


class Blog:
    def __init__(self):
        self._user_id = None
        self._user_name = None
        self._profile_cache = None

    def clear_session(self):
        self._user_id = None
        self._user_name = None
        self._profile_cache = None

    @property
    def user_id(self):
        return self._user_id

    @property
    def user_name(self):
        return self._user_name

    # -------------------- ACCOUNT CREATION --------------------- #
    def create_account(self, first_name, last_name, contact, email, bio, user_name, password):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "SELECT id FROM user_info WHERE user_name=%s OR email=%s",
                (user_name, email),
            )
            if cursor.fetchone():
                return False

            cursor.execute(
                """
                INSERT INTO user_info (first_name, last_name, contact, email, bio, user_name, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (first_name, last_name, contact, email, bio, user_name, "user"),
            )
            user_id = cursor.lastrowid

            hashed = _hash_password(password)
            cursor.execute(
                "INSERT INTO user_pass (user_id, password) VALUES (%s, %s)",
                (user_id, hashed),
            )

            db.commit()
            self._user_id = user_id
            self._user_name = user_name
            return True

        except Exception as e:
            db.rollback()
            print("❌ create_account error:", e)
            return False

        finally:
            cursor.close()

    # ---------LOGIN
    def log_in(self, user_name, password):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                SELECT u.id AS user_id, u.user_name, p.password
                FROM user_info u
                JOIN user_pass p ON u.id = p.user_id
                WHERE u.user_name = %s
                """,
                (user_name,),
            )

            user_data = cursor.fetchone()
            if not user_data:
                return False

            stored_hash = user_data["password"]
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")

            if not _check_password(password, stored_hash):
                return False

            self._user_id = user_data["user_id"]
            self._user_name = user_data["user_name"]
            self._profile_cache = None
            return True

        except Exception as e:
            print("❌ login error:", e)
            return False

        finally:
            cursor.close()

    # ----- PROFILE 
    def get_user_profile(self):
        if not self._user_id:
            return None
        if self._profile_cache:
            return self._profile_cache

        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                SELECT id, first_name, last_name, email, contact, bio,
                       user_name, created_at, role
                FROM user_info
                WHERE id=%s
                """,
                (self._user_id,),
            )
            data = cursor.fetchone()
            self._profile_cache = data
            return data

        except Exception as e:
            print("❌ get_user_profile error:", e)
            return None

        finally:
            cursor.close()

    
    #------ BLOG OPERATIONS
   
    def add_blog(self, title, main_blog):
        if not self._user_id:
            return False

        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO blog (title, main_blog, created_by) VALUES (%s, %s, %s)",
                (title, main_blog, self._user_id),
            )
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print("❌ add_blog error:", e)
            return False

        finally:
            cursor.close()

    def view_user_blogs(self):
        if not self._user_id:
            return []

        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "SELECT * FROM blog WHERE created_by=%s AND dlt=0 ORDER BY created_at DESC",
                (self._user_id,),
            )
            return cursor.fetchall()

        except Exception as e:
            print("❌ view_user_blogs error:", e)
            return []

        finally:
            cursor.close()

    def get_all_blogs(self):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                SELECT b.*, u.user_name, u.first_name, u.last_name
                FROM blog b
                LEFT JOIN user_info u ON b.created_by = u.id
                WHERE b.dlt=0
                ORDER BY b.created_at DESC
                """
            )
            return cursor.fetchall()

        except Exception as e:
            print("❌ get_all_blogs error:", e)
            return []

        finally:
            cursor.close()

    def update_blog(self, blog_id, title, main_blog):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                UPDATE blog
                SET title=%s, main_blog=%s
                WHERE id=%s AND created_by=%s
                """,
                (title, main_blog, blog_id, self._user_id),
            )
            db.commit()
            return cursor.rowcount > 0

        except Exception as e:
            db.rollback()
            print("❌ update_blog error:", e)
            return False

        finally:
            cursor.close()

    def soft_delete_blog(self, blog_id):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "UPDATE blog SET dlt=1 WHERE id=%s AND created_by=%s",
                (blog_id, self._user_id),
            )
            db.commit()
            return cursor.rowcount > 0

        except Exception as e:
            db.rollback()
            print("❌ soft_delete_blog error:", e)
            return False

        finally:
            cursor.close()

    def restore_blog(self, blog_id):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "UPDATE blog SET dlt=0 WHERE id=%s AND created_by=%s",
                (blog_id, self._user_id),
            )
            db.commit()
            return cursor.rowcount > 0

        except Exception as e:
            db.rollback()
            print("❌ restore_blog error:", e)
            return False

        finally:
            cursor.close()

    def permanent_delete_blog(self, blog_id):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "DELETE FROM blog WHERE id=%s AND created_by=%s",
                (blog_id, self._user_id),
            )
            db.commit()
            return cursor.rowcount > 0

        except Exception as e:
            db.rollback()
            print("❌ permanent_delete_blog error:", e)
            return False

        finally:
            cursor.close()

    def view_deleted_blogs(self):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "SELECT * FROM blog WHERE created_by=%s AND dlt=1 ORDER BY created_at DESC",
                (self._user_id,),
            )
            return cursor.fetchall()

        except Exception as e:
            print("❌ view_deleted_blogs error:", e)
            return []

        finally:
            cursor.close()

    # 
    #  COMMENTS                             #
  
    def add_comment(self, blog_id, text):
        if not self._user_id:
            return False

        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO blog_comments (blog_id, user_id, comment_text)
                VALUES (%s, %s, %s)
                """,
                (blog_id, self._user_id, text),
            )
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print("❌ add_comment error:", e)
            return False

        finally:
            cursor.close()

    def get_comments(self, blog_id):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                SELECT c.*, u.user_name, u.first_name, u.last_name
                FROM blog_comments c
                LEFT JOIN user_info u ON c.user_id = u.id
                WHERE c.blog_id=%s
                ORDER BY c.created_at ASC
                """,
                (blog_id,),
            )
            return cursor.fetchall()

        except Exception as e:
            print("❌ get_comments error:", e)
            return []

        finally:
            cursor.close()

    #                         REACTIONS                             #
 
    def set_reaction(self, blog_id, reaction):
        if reaction not in ("like", "dislike"):
            return False

        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "DELETE FROM blog_reactions WHERE blog_id=%s AND user_id=%s",
                (blog_id, self._user_id),
            )

            cursor.execute(
                """
                INSERT INTO blog_reactions (blog_id, user_id, reaction)
                VALUES (%s, %s, %s)
                """,
                (blog_id, self._user_id, reaction),
            )

            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print("❌ set_reaction error:", e)
            return False

        finally:
            cursor.close()

    def get_reaction_summary(self, blog_id):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    SUM(CASE WHEN reaction='like' THEN 1 ELSE 0 END) AS likes,
                    SUM(CASE WHEN reaction='dislike' THEN 1 ELSE 0 END) AS dislikes
                FROM blog_reactions
                WHERE blog_id=%s
                """,
                (blog_id,),
            )
            counts = cursor.fetchone() or {}
            likes = int(counts.get("likes", 0) or 0)
            dislikes = int(counts.get("dislikes", 0) or 0)

            cursor.execute(
                "SELECT reaction FROM blog_reactions WHERE blog_id=%s AND user_id=%s",
                (blog_id, self._user_id),
            )
            row = cursor.fetchone()
            user_reaction = row["reaction"] if row else None

            return {
                "likes": likes,
                "dislikes": dislikes,
                "user_reaction": user_reaction,
            }

        except Exception as e:
            print("❌ get_reaction_summary error:", e)
            return {"likes": 0, "dislikes": 0, "user_reaction": None}

        finally:
            cursor.close()

    # ============================================================= #
    #                        DASHBOARD METRICS                      #
    # ============================================================= #
    def get_dashboard_metrics(self):
        db = db_client.get_db()
        cursor = db.cursor()

        try:
            # user active posts
            cursor.execute(
                "SELECT COUNT(*) AS c FROM blog WHERE created_by=%s AND dlt=0",
                (self._user_id,),
            )
            active = cursor.fetchone().get("c", 0)

            # user trashed posts
            cursor.execute(
                "SELECT COUNT(*) AS c FROM blog WHERE created_by=%s AND dlt=1",
                (self._user_id,),
            )
            trashed = cursor.fetchone().get("c", 0)

            # community posts
            cursor.execute("SELECT COUNT(*) AS c FROM blog WHERE dlt=0")
            community = cursor.fetchone().get("c", 0)

            return {
                "active": active,
                "trashed": trashed,
                "community": community,
            }

        except Exception as e:
            print("❌ get_dashboard_metrics error:", e)
            return {"active": 0, "trashed": 0, "community": 0}

        finally:
            cursor.close()

    # ============================================================= #
    #                         ADMIN ROLE                            #
    # ============================================================= #
    def is_admin(self):
        profile = self.get_user_profile()
        if not profile:
            return False
        return (profile.get("role") or "").lower() == "admin"

    def list_users(self):
        if not self.is_admin():
            return []

        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                SELECT id, user_name, first_name, last_name, email, contact, role, created_at
                FROM user_info
                ORDER BY created_at DESC
                """
            )
            return cursor.fetchall()

        except Exception as e:
            print("❌ list_users error:", e)
            return []

        finally:
            cursor.close()

    def set_user_role(self, user_id, role):
        if not self.is_admin():
            return False
        if role not in ("admin", "user"):
            return False

        db = db_client.get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "UPDATE user_info SET role=%s WHERE id=%s",
                (role, user_id),
            )
            db.commit()
            return cursor.rowcount > 0

        except Exception as e:
            db.rollback()
            print("❌ set_user_role error:", e)
            return False

        finally:
            cursor.close()
