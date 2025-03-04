import { Container } from "@mui/material";
import Menu from "./menu";

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Menu />
      <Container sx={{ marginTop: 4 }}>{children}</Container>
    </>
  );
};

export default Layout;
