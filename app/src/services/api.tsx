import axios from 'axios';
const usuariosMock = [
  { id: 1, nome: "Alice" },
  { id: 2, nome: "Bob" },
  { id: 3, nome: "Carlos" },
];

const noticiasMock = [
  {
    id_noticia: "23kj2l3123klj9djladdsds234g",
    titulo: "Notícia 1",
    subtitulo: "Subtítulo da Notícia 1",
    url: "www.noticia.com.br/noticia1",
  },
  {
    id_noticia: "98asd7f98a7sdf89a7sdf89a7sd",
    titulo: "Notícia 2",
    subtitulo: "Subtítulo da Notícia 2",
    url: "www.noticia.com.br/noticia2",
  },
  {
    id_noticia: "12kj3h1k2j3h1k2j3h1k2j3h1k2j",
    titulo: "Notícia 3",
    subtitulo: "Subtítulo da Notícia 3",
    url: "www.noticia.com.br/noticia3",
  },
];


let api_url = process.env.API; 

export const fetchUsuarios = async () => {
  
  if (api_url === undefined) {
    api_url = "http://localhost:8001";
  }

  try {
    const response = await axios.get(api_url+ '/users');
    return response.data.users;
  } catch (error) {
      console.error('Erro ao buscar usuários:', error);
      throw new Error('Erro ao buscar usuários');
  }
};

export const postUsuario = async (usuario: any) => {
  
  if (api_url === undefined) {
    api_url = "http://localhost:8001";
  }

  try {
    const response = await axios.post(api_url + '/add_user', usuario);
    return true;
  } catch (error) {
      console.error('Erro ao cadastrar usuário:', error);
      throw new Error('Erro ao cadastrar usuário');
  }
};

export const postNoticia= async (noticia: any) => {
  
  if (api_url === undefined) {
    api_url = "http://localhost:8001";
  }

  try {
    const response = await axios.post(api_url + '/add_news', noticia);
    return true;
  } catch (error) {
    console.error('Erro ao cadastrar usuário:', error);
    throw new Error('Erro ao cadastrar usuário');
  }
};
export const fetchNoticiasRecomendadas = async (user_id : any) => {
  try {
    const response = await axios.post(api_url+ '/predict', { 
        user_id : user_id,
        use_heuristic : false,
        qtty_recommendations : 5
    });

    return response.data.prediction;
  } catch (error) {
      console.error('Erro ao realizar predição:', error);
      throw new Error('Erro ao predizer notícias');
  }
};

export const fetchReadNews = async (user_id : any, news_id: any) => {
  try {
    const response = await axios.post(api_url+ '/read_news', { 
        user_id : user_id,
        news_id : news_id
    });
    return response.data.read;
  } catch (error) {
      console.error('Erro ao registrar acesso:', error);
      throw new Error('Erro ao registrar acesso');
  }
};
