import React, { useState } from "react";
import { useRouter } from 'next/router';
import { TextField, Button, Container, Typography } from "@mui/material";
import { postUsuario } from "../services/api";
const CadastrarUsuario = () => {
  const [nome, setNome] = useState("");

  const router = useRouter(); 

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    let success = await postUsuario({
      nome
    });
  
    if(success){
      alert("Usuario cadastrado com sucesso!");
      router.push('/');
    }else{
      alert("Erro ao cadastrar usuario!");
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Cadastrar Usuario
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Nome"
          variant="outlined"
          fullWidth
          margin="normal"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />
        <Button type="submit" variant="contained" color="primary" fullWidth>
          Cadastrar Usuario
        </Button>
      </form>
    </Container>
  );
};

export default CadastrarUsuario;
