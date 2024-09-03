CurrentDeck <- read.csv(file="../files/branded-despia-deck-list.csv", header=TRUE)

cardList <- CurrentDeck$Card.names

hands <- data.frame(c("card1", "card2", "card3", "card4", "card5"))
for(hand in 1:1000){
    fiveCards<-sample(cardList, 5)
    hands[hand] <- fiveCards
}

write.csv(t(hands), file="../files/branded-despia-result-hands.csv")

DataRatings <- read.csv(file="../files/branded-despia-with-ratings.csv", header=TRUE)

ratings <- DataRatings$Ratings

mean(ratings)

var(raitings)

hist(ratings)
