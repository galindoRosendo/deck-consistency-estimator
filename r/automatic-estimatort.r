# Definir el mazo con varias cartas clave
deckData <- read.csv("../files/branded-despia-deck-list.csv", header=TRUE)

currentDeck <- deckData$Card.names

set.seed(123)  # Establecer una semilla para reproducibilidad

# Función para simular una mano inicial
simulateHand <- function(deck, hand_size = 5) {
  sample(deck, hand_size, replace = FALSE)
}

# Función para verificar múltiples cartas clave
containsMultipleKeyCards <- function(
  hand, 
  keyCards1 = c("Branded Fusion", "Crossout Designator"),
  keyCards2 = c("Aluber the Jester of Despia", "Crossout Designator"),
  keyCards3 = c("Branded Opening", "Crossout Designator"),
  keyCards4 = c("Despian Tragedy", "Allure of Darkness", "Crossout Designator"),
  keyCards5 = c("Despian Tragedy", "Foolish Burial", "Crossout Designator"),
  keyCards6 = c("Despian Tragedy", "Gold Sarcophagus", "Crossout Designator"),
  keyCards7 = c("Fallen of Albaz", "Blazing Cartesia the Virtuous")
  ) {
    if(all(sapply(keyCards1, function(card) card %in% hand))) { TRUE }
    else if(all(sapply(keyCards2, function(card) card %in% hand))) { TRUE }
    else if(all(sapply(keyCards3, function(card) card %in% hand))) { TRUE }
    else if(all(sapply(keyCards4, function(card) card %in% hand))) { TRUE }
    else if(all(sapply(keyCards5, function(card) card %in% hand))) { TRUE }
    else if(all(sapply(keyCards6, function(card) card %in% hand))) { TRUE }
    else if(all(sapply(keyCards7, function(card) card %in% hand))) { TRUE }
    else {FALSE}
}

# Número de simulaciones
nSimulations <- 100000
successes <- 0

for (i in 1:nSimulations) {
  hand <- simulateHand(currentDeck)
  if (containsMultipleKeyCards(hand)) {
    successes <- successes + 1
  }
}

# Calcular la proporción de manos consistentes
consistency <- successes / nSimulations * 100
print(consistency)