import { AppBar, Toolbar, Button } from "@mui/material";
import Link from "next/link";

const Menu = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Link href="/" passHref>
          <Button
            color="inherit"
            sx={{
              color: "white",
              backgroundColor: "blue",
              fontWeight: "bold",
              "&:hover": { backgroundColor: "darkblue" },
            }}
          >
            <span>Início</span>
          </Button>
        </Link>
        <Link href="/usuarios" passHref>
          <Button
            color="inherit"
            sx={{
              color: "white",
              backgroundColor: "blue",
              fontWeight: "bold",
              "&:hover": { backgroundColor: "darkblue" },
            }}
          >
            <span>Usuários</span>
          </Button>
        </Link>
        <Link href="/noticias-populares" passHref>
          <Button
            color="inherit"
            sx={{
              color: "white",
              backgroundColor: "blue",
              fontWeight: "bold",
              "&:hover": { backgroundColor: "darkblue" },
            }}
          >
            <span>Notícias Populares</span>
          </Button>
        </Link>
        <Link href="/noticias-recomendadas" passHref>
          <Button
            color="inherit"
            sx={{
              color: "white",
              backgroundColor: "blue",
              fontWeight: "bold",
              "&:hover": { backgroundColor: "darkblue" },
            }}
          >
            <span>Recomendadas</span>
          </Button>
        </Link>
        <Link href="/cadastrar-noticia" passHref>
          <Button
            color="inherit"
            sx={{
              color: "white",
              backgroundColor: "blue",
              fontWeight: "bold",
              "&:hover": { backgroundColor: "darkblue" },
            }}
          >
            <span>Cadastrar Notícia</span>
          </Button>
        </Link>
      </Toolbar>
    </AppBar>
  );
};

export default Menu;
