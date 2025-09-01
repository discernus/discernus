library(ggplot2)
library(lubridate)
library(scales)
library(tm)
library(stringr)
library(RColorBrewer)
library(wordcloud)
library(syuzhet)
library(reshape2)
library(dplyr)
library(twitteR)
library(tidyverse)
library(extrafont)
library(devtools)
library(tidytext)
library(cluster)
library(dendextend)
library(factoextra)
library(FactoMineR)
library(ape)
library(ggdendro)
library(igraph)
library(ggsci)
library(gridExtra)
library(ggpubr)
library(textclean)
library(textstem)
library(text2vec)
library(Rtsne)
library(plotly)
library(ggrepel)
library(SnowballC)
library(e1071)
library(plyr)
library(ggthemes)
library(ggridges)
library(NLP)

muslimban_full$created_at = as.POSIXct(muslimban_full$created_at, format = "%a %b %d %H:%M:%S %z %Y", tz= "America/New_York")
muslimban_full$mday = mday(muslimban_full$created_at)


muslimban_full$mday <- as.Date(muslimban_full$created_at, "%d-%b")

timeline.f = ggplot(time., aes(x = Day, y = Tweet)) +
  geom_line()+
  theme(plot.title = element_text(size = 15, face = "bold"))+
  ylab("Numer of Tweets") +
  scale_y_continuous(breaks=seq(0, 700000, by = 50000))+
  scale_x_date(limits=as.Date(c("2018-02-08", "2018-03-14")), date_breaks="1 day", labels = date_format("%d-%b"))

timeline.f + theme_fivethirtyeight() +
  ylab("Number of Tweets")+
  theme(axis.text.x = element_text(angle=90, vjust=0.5))


## evolution per hours (Jan 27, 2017)

Jan29$created_at = as.POSIXct(Jan29$created_at, format = "%a %b %d %H:%M:%S %z %Y", tz= "America/New_York")
Jan29$timeonly <- as.numeric(Jan29$created_at - trunc(retweets_muslim_jan$created_at, "days"))
class(Jan29$timeonly) <- "POSIXct"

march1.f = ggplot(Jan29, aes(x=created_at))+
  geom_histogram(aes(fill= ..count..))+
  theme(legend.position = "none") +
  xlab("Time") + ylab("Number of tweets") + 
  scale_x_datetime(breaks = date_breaks("1 hours"), labels = date_format("%H:00"))+
  scale_fill_gradient(low = "lightgrey", high = "gray11")+
  theme(axis.text.x = element_text(angle=90, vjust=0.5))+
  theme(legend.position = "none") +
  theme(plot.title = element_text(size = 15, face = "bold"))
  

  #geom_text(data=March1[10000, ], y=19000, label="Our Steel and Aluminum industries (and many others) have been decimated \n by decades of unfair trade and bad policy with countries from around the world. \n We must not let our country companies and workers be taken advantage of any longer. \n We want free fair and SMART TRADE! \n @realDonaldTrump", fontface="bold", vjust=1, size=2.3)+
  #geom_segment(x=44000, y=0, xend=44000, yend=15000, linetype="dotted")



march1.f


## cleaning tweets

muslimban_trumpers$text = str_replace_all(muslimban_trumpers$text, "@\\w+", "")
muslimban_trumpers$text = gsub("&amp", "", muslimban_trumpers$text)
muslimban_trumpers$text <- iconv(muslimban_trumpers$text, "latin1", "ASCII", sub="")
corpus <- VCorpus(VectorSource(muslimban_trumpers$text))
removeURL = function(x) gsub("http[[:alnum:]]","",x)
corpus <- tm_map(corpus, content_transformer(removeURL))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removePunctuation) 
corpus <- tm_map(corpus, removeWords, stopwords("english")) #remove stopwords
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, removeWords, c("indeed", "needs", "new", "like", "breaking", "will", "said", "says", "just", "even", "now", "one", "can", "dont", "look"))
#corpus <- tm_map(corpus, removeWords, c("good", "president", "obama", "hockey", "even", "many", "olympic", "start", "much", "just", "another", "last", "calls", "way", "join", "next", "way", "going", "still", "back", "people", "russias", "putins", "support", "presid", "uuauuuudu", "udu", "ask", "httpc", "htt", "photo", "move", "year", "must", "tell", "week", "dec", "let", "eas", "meet", "maidan", "gold", "day", "time", "video", "watch", "digitalmaidan", "today", "live", "peopl", "cdnpoli", "militari", "crisi", "protest", "canada", "kiev", "kyiv", "get", "one", "new", "dont", "news","can", "use", "putin", "russia", "ukrain", "call", "show", "need", "via", "updat", "march", "feb", "want", "rt", "rbssfinancialservicesandrealestatenew", "may", "say", "know", "bondsnew", "marketnews", "marketsnew", "usdollarrpt", "stock", "olymp", "look", "give", "make", "talk", "like", "now","tcot", "take"))

muslimbantdm <- TermDocumentMatrix(corpus)
muslimbantdm = removeSparseTerms(muslimbantdm, .9999)

musdtfreq=rowSums(as.matrix(muslimbantdm))
mushigh.freq = tail(sort(musdtfreq),n=50)
msuhfp.df = as.data.frame(sort(mushigh.freq))
msuhfp.df$names <- rownames(msuhfp.df) 

musdf = ggplot(msuhfp.df, aes( x = reorder(names, mushigh.freq), mushigh.freq)) +
  geom_bar(stat="identity") + coord_flip() + 
  xlab("Terms") + ylab("Frequency") +
  ggtitle("Muslim ban") +
  theme(axis.text.y = element_text(size=12.5))

musdf

write.csv(ukrhfp.df, "muslimwords.csv", row.names = FALSE)

### GloVE testing - word embeding

stopwords <- c(tm::stopwords("english"), "ar", "tell", "know", "sai", "isnt", "way", "youre", "retweet", "th", "actually",  "say", "will", "rt", "s", "want", "video", "amp", "get", "wor", "indeed", "watch",  "needs", "new", "like", "breaking", "will", "said", "says", "just", "even", "now", "one", "can", "dont", "look")

muslimban_trumpers$text <- gsub("http.*","",  muslimban_trumpers$text)
muslimban_trumpers$text <- str_replace_all(muslimban_trumpers$text ,"@[a-z,A-Z]*","") 
muslimban_trumpers$text = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", muslimban_trumpers$text) 
muslimban_trumpers$text = gsub("@\\w+", "", muslimban_trumpers$text) # regex for removing @user
muslimban_trumpers$text = gsub("[[:punct:]]", "", muslimban_trumpers$text) # regex for removing punctuation mark
muslimban_trumpers$text = gsub("[[:digit:]]", "", muslimban_trumpers$text) # regex for removing numbers
muslimban_trumpers$text = gsub("http\\w+", "", muslimban_trumpers$text) # regex for removing links
muslimban_trumpers$text = gsub("\n", " ", muslimban_trumpers$text)  ## regex for removing new line (\n)
muslimban_trumpers$text = gsub("[ \t]{2,}", " ", muslimban_trumpers$text) ## regex for removing two blank space
muslimban_trumpers$text =  gsub("[^[:alnum:]///' ]", " ", muslimban_trumpers$text)     # keep only alpha numeric 
muslimban_trumpers$text =  iconv(muslimban_trumpers$text, "latin1", "ASCII", sub="")   # Keep only ASCII characters
muslimban_trumpers$text = gsub("^\\s+|\\s+$", "", muslimban_trumpers$text)  # Remove leading and trailing white space
muslimban_trumpers$text = stopwords(muslimban_trumpers$text)
muslimban_trumpers$text = stem_strings(muslimban_trumpers$text, language = "porter")



# Create iterator over tokens
N = 1000

it = itoken(muslimban_trumpers$text, tolower, tokenizer = word_tokenizer)

v = create_vocabulary(it, stopwords = stopwords)

#remove very common and uncommon words

v <- prune_vocabulary(v, term_count_min = 9000L)

# Use our filtered vocabulary

vectorizer <- vocab_vectorizer(v)

# use window of 5 for context words

dtm = create_dtm(it, vectorizer)

tcm <- create_tcm(it, vectorizer, skip_grams_window = 5L)

glove = GlobalVectors$new(word_vectors_size = 50, vocabulary = v, x_max = 10)

wv_main = glove$fit_transform(tcm, n_iter = 150, convergence_tol = 0.01)

wv_context = glove$components

dim(wv_context)

word_vectors = wv_main + t(wv_context)



### T-sne plotting for word2vec representation

### Plot tensorflow of word embedding

count = v$term_count

tsne <- Rtsne(word_vectors, perplexity = 15, pca = FALSE)

tsne_plot <- tsne$Y %>%
  as.data.frame() %>%
  mutate(word = row.names(word_vectors)) %>%
  ggplot(aes(x = V1, y = V2, label = word)) + 
  ggtitle("t-SNE Russian cluster tweets - < 175")+
  geom_point(aes(V1, V2, size = count, alpha =.1), color = "#990000")+
  geom_text_repel(size = 4)+
  scale_size(range = c(.5, 50))+
  theme(legend.position = "none")

tsne_plot


## Curating the database for analysis with both t-SNE and PCA

Labels<-train$label
train$label<-as.factor(train$label)

## for plotting

colors = rainbow(length(unique(train$label)))
names(colors) = unique(train$label)

## Executing the algorithm on curated data

tsne <- Rtsne(train[,-1], dims = 2, perplexity=30, verbose=TRUE, max_iter = 500)
exeTimeTsne<- system.time(Rtsne(train[,-1], dims = 2, perplexity=30, verbose=TRUE, max_iter = 500))

## Plotting

plot(tsne$Y, t='n', main="tsne")
text(tsne$Y, labels=train$label, col=colors[train$label])

### tsne --- ploting graph

tsne <- Rtsne(word_vectors[2:50,], perplexity = 10, pca = FALSE)

tsne_plot <- tsne$Y %>%
  as.data.frame() %>%
  mutate(word = row.names(word_vectors)[2:50]) %>%
  ggplot(aes(x = V1, y = V2, label = word)) + 
  geom_text(size = 3)

tsne_plot

### cool tsne 

library(mlbench)
library(ggthemes)
library(plotly)
library(dplyr)

# Run t-SNE with a seed for reproducibility
set.seed(101)
tsne_out <- Rtsne(word_vectors[2:50,], dims = 3, max_iter = 1000, perplexity = 10, pca = FALSE)


# Prepare a data frame for plotting
d_tsne <- data.frame(tsne_out$Y, Class = Vehicle$Class)
colnames(d_tsne) <- c("x", "y", "z", "Class")

# Create a 3D Scatter plot using plotly
p <- 
  plot_ly(d_tsne, x = x, y = y, z = z, type = "scatter3d", group = Class, mode = "markers") %>%
  layout(title = "t-SNE on 'Words'")
p