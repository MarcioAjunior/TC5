import axios from 'axios';

let api_url = process.env.API; 

if (api_url === undefined) {
  api_url = "http://127.0.0.1:8001";
}
export const fetchUsuarios = async () => {

  console.log(api_url + '/users');



  try {
    const response = await axios.get(api_url+'/users');
    console.log(api_url + '/users');
    return response.data.users;
  } catch (error) {
      console.error('Erro ao buscar usuários:', error);
      throw new Error('Erro ao buscar usuários');
  }
};

export const postUsuario = async (usuario: any) => {
  
  try {
    const response = await axios.post(api_url + '/add_user', usuario);
    return true;
  } catch (error) {
      console.error('Erro ao cadastrar usuário:', error);
      throw new Error('Erro ao cadastrar usuário');
  }
};

export const postNoticia= async (noticia: any) => {
  
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
