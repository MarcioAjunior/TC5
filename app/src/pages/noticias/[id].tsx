import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Slider from "react-slick";
import {
  Typography,
  Card,
  CardContent,
  CardMedia,
  Container,
  Box,
  Button,
  IconButton,
  Grid,
  FormControlLabel,
  Switch
} from "@mui/material";
import Link from "next/link";
import { fetchNoticiasRecomendadas, fetchReadNews } from "../../services/api";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";

const NoticiasRecomendadas = () => {

  const router = useRouter();
  const { id } = router.query;

  const [checked, setChecked] = useState(false); // Estado para controlar o switch

  const [noticias, setNoticias] = useState<
    { id: string; titulo: string; subtitulo: string; url: string }[]
  >([]);

  // noticia que es sendo lida
  const [noticiaDestaque, setNoticiaDestaque] = useState<{
    id: string;
    titulo: string;
    subtitulo: string;
    url: string;
  } | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Carregar notícias recomendadas
  const carregarNoticias = async () => {
    if (!id) return;
    try {
      const data = (await fetchNoticiasRecomendadas(id)) as {
        id: string;
        titulo: string;
        subtitulo: string;
        url: string;
      }[];
      setNoticias(data);
      setNoticiaDestaque(data[0]);
    } catch (err) {
      setError("Erro ao carregar notícias recomendadas");
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    carregarNoticias();
  }, [id]);

  const handleChangeSwitch = async(event: React.ChangeEvent<HTMLInputElement>) => {
    setChecked(event.target.checked);
    if (!checked) {
      console.log(noticiaDestaque?.titulo)
      console.log(noticiaDestaque?.id)
      let success = await fetchReadNews(
        id,
        noticiaDestaque?.id
      );
      if (success) {
        alert("Noticia marcada como lida!");
        try {
          const data = (await fetchNoticiasRecomendadas(id)) as {
            id: string;
            titulo: string;
            subtitulo: string;
            url: string;
          }[];
          setNoticias(data);
        } catch (err) {
          setError("Erro ao carregar notícias recomendadas");
        } finally {
          setChecked(false);
          setLoading(false);
        }

      } else {
        alert("Erro ao marcar noticia como lida!");
      }
    } 
  };
  const handleNoticiaClick = async (
    noticia: React.SetStateAction<{
      id: string;
      titulo: string;
      subtitulo: string;
      url: string;
    } | null>
  ) => {
    setNoticiaDestaque(noticia);
    try {
      const data = (await fetchNoticiasRecomendadas(id)) as {
        id: string;
        titulo: string;
        subtitulo: string;
        url: string;
      }[];
      setNoticias(data);
    } catch (err) {
      setError("Erro ao carregar notícias recomendadas");
    } finally {
      setChecked(false);
      setLoading(false);
    }
    
  };

  if (loading) {
    return <Typography>Carregando...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 4,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
        },
      },
    ],
  };

  return (
    <Box
      sx={{
        backgroundColor: "background.default",
        minHeight: "100vh",
        padding: "20px",
      }}
    >
      <Container>
        <IconButton
          onClick={() => router.back()}
          style={{ marginBottom: "20px" }}
        >
          <ArrowBackIosIcon />
        </IconButton>

        {noticiaDestaque && (
          <Box mb={10}>
            <Typography
              variant="h3"
              gutterBottom
              sx={{ fontWeight: "bold", color: "text.primary" }}
            >
              {noticiaDestaque.titulo}
            </Typography>
            <Typography
              variant="subtitle1"
              gutterBottom
              sx={{ color: "text.secondary" }}
            >
              {noticiaDestaque.subtitulo}
            </Typography>
            <Typography variant="body1" sx={{ color: "text.primary" }}>
              Link da Notícia: {noticiaDestaque.url}
            </Typography>
          </Box>
        )}

        {/* Carrossel de Notícias Recomendadas */}
        <Grid container spacing={4}> {/* Espaçamento entre as colunas */}

          <Typography
            variant="h4"
            gutterBottom
            sx={{ fontWeight: "bold", marginTop: "40px", color: "text.primary" }}
          >
            Mais notícias para você
          </Typography>
          <FormControlLabel
            control={
              <Switch
                checked={checked}
                onChange={handleChangeSwitch}
                color="primary"
                sx={{ marginTop: "2px", marginLeft: 67 }}
              />
            }
            label="Marcar noticia como lida"
            sx={{ marginTop: 2 }}
          />
        </Grid>

        {noticias.length > 0 ? (
          <Slider {...settings}>
            {noticias.map((noticia) => (
              <div key={noticia.id}>
                <Card
                  onClick={() => handleNoticiaClick(noticia)}
                  style={{ margin: "10px", cursor: "pointer" }}
                  sx={{
                    borderRadius: "8px",
                    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                    transition: "transform 0.2s, box-shadow 0.2s",
                    "&:hover": {
                      transform: "scale(1.05)",
                      boxShadow: "0 8px 16px rgba(0, 0, 0, 0.2)",
                    },
                  }}
                >
                  <CardContent>
                    <Typography
                      variant="h6"
                      sx={{ fontWeight: "bold", color: "text.primary" }}
                    >
                      {noticia.titulo}
                    </Typography>
                    <Typography
                      variant="subtitle1"
                      color="text.secondary"
                      sx={{ color: "text.secondary" }}
                    >
                      {noticia.subtitulo}
                    </Typography>
                  </CardContent>
                </Card>
              </div>
            ))}
          </Slider>
        ) : (
          <Typography variant="body1" sx={{ color: "text.primary" }}>
            Nenhuma notícia recomendada encontrada.
          </Typography>
        )}
      </Container>
    </Box>
  );
};

export default NoticiasRecomendadas;
