import random

NOMES = {
    "Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Fernando", "Gabriela", "Hugo", "Isabela", "João",
    "Karina", "Lucas", "Mariana", "Nathan", "Olivia", "Paulo", "Quezia", "Rafael", "Sofia", "Tiago",
    "Ursula", "Vitor", "Wellington", "Ximena", "Yago", "Zara", "Alice", "Benjamin", "Camila", "Diego",
    "Elisa", "Fábio", "Giovana", "Heitor", "Ingrid", "Júlio", "Katia", "Leandro", "Mirela", "Norberto",
    "Orlando", "Priscila", "Quirino", "Raquel", "Samuel", "Tainá", "Ubirajara", "Valéria", "William", "Xavier",
    "Yasmin", "Zaqueu", "Adriana", "Bernardo", "Cecília", "Douglas", "Esther", "Felipe", "Gisele", "Henrique",
    "Ivana", "Jonas", "Kelly", "Leonardo", "Melissa", "Nicolas", "Otávio", "Patrícia", "Quintino", "Rebeca",
    "Simone", "Tatiane", "Ulisses", "Vanessa", "Wesley", "Xandra", "Yuri", "Zélia", "André", "Bianca", "Cristiano",
    "Diana", "Enzo", "Fernanda", "Gustavo", "Helena", "Ícaro", "Jéssica", "Kleber", "Lorena", "Matheus", "Natália",
    "Orfeu", "Paloma", "Quésia", "Rodrigo", "Selma", "Tarcísio", "Uriel", "Vitória", "Wallace", "Xênia", "Yvone",
    "Zilda", "Augusto", "Bárbara", "Cauê", "Débora", "Emanuel", "Flávia", "Gilberto", "Hilda", "Ísis", "Jefferson",
    "Karen", "Luana", "Maurício", "Neide", "Osvaldo", "Pedro", "Quitéria", "Ricardo", "Samantha", "Tamara", "Ugo",
    "Vilma", "Wanderley", "Xisto", "Ylana", "Zoroastro", "Aline", "Brenda", "Caio", "Denise", "Elton", "Fabiana",
    "Geraldo", "Heloísa", "Ítalo", "Joana", "Kevin", "Lívia", "Marcelo", "Nair", "Olavo", "Paula", "Quirina", "Roberto",
    "Sandro", "Tereza", "Urbano", "Vânia", "Wilson", "Xande", "Yasmina", "Zenaide"
}

SOBRENOMES = {
    "Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima", "Carvalho", "Ferreira", "Rodrigues", "Almeida",
    "Costa", "Gomes", "Martins", "Barros", "Vieira", "Mendes", "Nunes", "Moreira", "Teixeira", "Cavalcante",
    "Monteiro", "Dias", "Correia", "Azevedo", "Ribeiro", "Cardoso", "Freitas", "Duarte", "Borges", "Araújo",
    "Andrade", "Moura", "Xavier", "Figueiredo", "Cunha", "Torres", "Rezende", "Siqueira", "Batista", "Neves"
}

def generate_random_name():
    return f"{random.choice(tuple(NOMES))} {random.choice(tuple(SOBRENOMES))}"