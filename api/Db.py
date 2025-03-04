import psycopg2
from psycopg2.extras import DictCursor
from typing import List, Dict

class DbManager:
    _instance = None

    def __new__(cls, dict_connection: str):
        """Singleton: Garante que só existe uma instância da classe."""
        if cls._instance is None:
            cls._instance = super(DbManager, cls).__new__(cls)
            cls._instance._init_db(dict_connection)
        return cls._instance

    def _init_db(self, dict_connection: str):
        """Inicializa a conexão com o PostgreSQL."""
        self.conn = psycopg2.connect(**dict_connection)
        self.conn.autocommit = True

    def add_user(self, user_id, nome, embedding):
        """Adiciona um usuário ao banco."""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (id, nome, embedding) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;",
                (user_id, nome, embedding)
            )
            self.conn.commit()

    def add_news(self, news_id, title, subtitile, body, url, embedding):
        """Adiciona uma notícia ao banco."""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO news (id, titulo, subtitulo, corpo_noticia, url, embedding) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
                (news_id, title, subtitile, body, url, embedding)
            )
            self.conn.commit()
    def get_user(self, user_id: str, users_ids : list) -> Dict:
        """Busca um usuário pelo ID."""
        if user_id is not None:
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
                return dict(cur.fetchone()) if cur.rowcount > 0 else {"error": "Usuário não encontrado"}
        if users_ids is not None:
            if users_ids == []:
                return []
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT id, nome FROM users WHERE id in %s;", (tuple(users_ids),))
                return [dict(row) for row in cur.fetchall()]

    def get_news(self, qtty_news = 1000, news_id: str = None, news_ids: list = None) -> Dict:
        """Busca uma notícia pelo ID ou as 100 últimas notícias ordenadas por data_publicacao."""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            if news_id:
                cur.execute("SELECT * FROM news WHERE id = %s;", (news_id,))
                return dict(cur.fetchone()) if cur.rowcount > 0 else {"error": "Notícia não encontrada"}
            elif news_ids:
                cur.execute("SELECT id, titulo, subtitulo, url FROM news WHERE id in %s;", (tuple(news_ids),))
                return [dict(row) for row in cur.fetchall()]
            else:
                cur.execute(f"SELECT id FROM news ORDER BY data_publicacao DESC LIMIT {qtty_news};")
                results = []
                for row in cur.fetchall():
                    results.append(str(row[0]))
                return results
            
    def make_access(self, user_id, embedding, engagement_score, news_id):
        """Atualiza o embedding de um usuário e adiciona um novo acesso."""
        with self.conn.cursor() as cur:
            cur.execute("UPDATE users SET embedding = %s WHERE id = %s;", (embedding, user_id))
            self.conn.commit()
            cur.execute("""
                        INSERT INTO 
                            access
                            (id_user, id_news, engagement) 
                        VALUES 
                            (%s, %s, %s)
                        RETURNING id;""", (user_id, news_id ,engagement_score))
            access_id = cur.fetchone()[0] 
            self.conn.commit()
            return access_id
    def get_latest_access(self, len_train) -> Dict:
        """Busca as últimas 10 notícias acessadas por um usuário."""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """select 
	                u.id, n.id, a.engagement, 0 as popularity_score,n.data_publicacao , n.embedding n_embedding , u.embedding u_embedding  
                from 
	                "access" a
	                join users u on a.id_user = u.id
	                join news n on a.id_news  = n.id
                order by 
	                a.id desc
                limit 
	                %s;""",
                (len_train,)
            )
            results = []
            for row in cur.fetchall():
                print(row)
                results.append(str(row))
            return results

