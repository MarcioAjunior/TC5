import React, { useEffect, useState } from "react";
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
} from "@mui/material";
import Link from "next/link";
import { fetchUsuarios } from "../services/api";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

const Home = () => {
  interface usuarios {
    id: number;
    nome: string;
  }

  const [Usuarios, setUsuarios] = useState<usuarios[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const carregarUsuarios = async () => {
      try {
        const data = await fetchUsuarios();
        setUsuarios(data as usuarios[]);
      } catch (err) {
        setError("Erro ao carregar usuarios");
      } finally {
        setLoading(false);
      }
    };

    carregarUsuarios();
  }, []);

  if (loading) {
    return <Typography>Carregando...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <div
      style={{
        padding: "20px",
        backgroundColor: "#121212",
        minHeight: "100vh",
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography
          variant="h4"
          gutterBottom
          sx={{ fontWeight: "bold", color: "primary.main" }}
        >
          Selecione um Usuario
        </Typography>
        <Box sx={{ textAlign: "center", marginTop: "20px", padding: "10px" }}>
        <Link href="/cadastrar-noticia" passHref>
            <Button
              variant="contained"
              color="primary"
              sx={{ fontWeight: "bold", marginRight: "10px"}}
            >
              Cadastrar Nova Notícia
            </Button>
          </Link>
          <Link href="/cadastrar-usuario" passHref>
            <Button
              variant="contained"
              color="primary"
              sx={{ fontWeight: "bold" }}
            >
              Cadastrar Usuario
            </Button>
          </Link>
        </Box>
      </Box>
      <Grid container spacing={3}>
        {Usuarios.map((Usuario) => (
          <Grid item key={Usuario.id} xs={12} sm={6} md={4}>
            <Link href={`/noticias/${Usuario.id}`} passHref>
              <Card
                sx={{
                  borderRadius: "12px",
                  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
                  transition: "transform 0.2s, box-shadow 0.2s",
                  "&:hover": {
                    transform: "scale(1.05)",
                    boxShadow: "0 8px 16px rgba(0, 0, 0, 0.3)",
                  },
                  background: "linear-gradient(145deg, #1e1e1e, #2c2c2c)",
                }}
              >
                <CardContent sx={{ display: "flex", alignItems: "center" }}>
                  <AccountCircleIcon
                    sx={{ fontSize: 40, color: "primary.main", mr: 2 }}
                  />
                  <div>
                    <Typography
                      variant="h5"
                      component="div"
                      sx={{ fontWeight: "bold", color: "primary.main" }}
                    >
                      {Usuario.nome}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{ color: "text.secondary" }}
                    >
                      ID: {Usuario.id}
                    </Typography>
                  </div>
                </CardContent>
              </Card>
            </Link>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default Home;
