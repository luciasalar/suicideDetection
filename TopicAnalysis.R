require(data.table)
require(fastDummies)
library(psych)
library(XLConnect)
require(stargazer)

## R Markdown

#the correlation between the frequency of posting and their risk level among redditors who have posted in a specific target subreddit. In the correlation 
#analysis, we exclude redditors who didn't post in the target subreddit because whether a redditor post in certain subreddit depends on whether they aware the existence of the sub. 
#The awareness of this information might not related be relevant to redditors' psychological traits and behavior. 

#We conduct a permutation correlation.  In each pairewise correlation, we scramble the row order of the variable. 


#Here we compute the correlation between each topic and each risk level. All the users a re 


#path = '/Users/lucia/phd_work/Clpsy'
path = '/home/lucia/phd_work/shareTask/'
setwd(path)
#labels <- read.csv("./data/clpsych19_training_data/crowd_train.csv")
post <- read.csv("./data/clpsych19_training_data/Btrain.csv")
SW <- read.csv("./data/clpsych19_training_data/Btrain_NoNoise_SW_LIWC.csv")
AllLiwc <- read.csv("./data/clpsych19_training_data/BtrainLiwc.csv")
# for class A, we need to filter out posts that talk about self 
allLabel <- read.csv("./data/clpsych19_training_data/crowd_train.csv")




#now we look at the top100 topics in all the users posts, divide the topics into groups and compute the topic counts 

NoSW <- subset(post, post$subreddit != 'SuicideWatch')
Top100 <- data.frame(table(NoSW$subreddit))
Top100<- Top100[order(-Top100$Freq),]
Top100 <- Top100[1:100, ]

GetTopicCor <- function(theme, themeName, bootstrapN){
  #generate a df for correlation
  GetDf<- function(theme, themeName){
    post$themeCount<- ifelse(post$subreddit == theme, 1, 0)
    # aggregate theme count on user level
    Seltheme <- post[post$themeCount == 1,]
    themes <- data.frame(table(Seltheme$user_id))
    colnames(themes) <- c('user_id', themeName)
    groupTheme <- merge(themes, groups, by = 'user_id', all.x = T)
    groupTheme <- groupTheme[!duplicated(groupTheme$user_id),]
    groupTheme$raw_label <- as.character(groupTheme$raw_label)
    groupTheme$raw_label[groupTheme$raw_label==""] <- 'NRisk'
    groupTheme$raw_label[groupTheme$raw_label== 'a'] <- 'LRisk'
    groupTheme$raw_label[groupTheme$raw_label== 'b'] <- 'MoRisk'
    groupTheme$raw_label[groupTheme$raw_label== 'c'] <- 'HRisk'
    groupTheme$raw_label[groupTheme$raw_label== 'd'] <- 'VHRisk'
    
    return(groupTheme)
  }
  #convert category to dummy vari then do correlation
  GetThemeCor <- function(groupTheme){
    # #permutation (sample the order of the data)
    # #set.seed(42)
    groupDum <- fastDummies::dummy_cols(groupTheme$raw_label)
    groupDumPer <- groupDum[sample(nrow(groupDum)),]
    corRe <- cor(groupDumPer[,-1], groupTheme[,2])
    return(corRe)
  }
  
  #permutation, times: number of iteration, theme:subreddit, get the most frequent value as result
  getMedian <- function(RiskLevel){
    NRisk <- c()
    for(i in 1:bootstrapN){
      groupTheme <- GetDf(theme, themeName)
      CorRe <- GetThemeCor(groupTheme)
      NRisk[[i]] <- round(CorRe[RiskLevel], digits = 2)
      mostFreq <- data.frame(sort(table(NRisk),decreasing=TRUE))
      mostFreq[,1] <- as.numeric(as.character(mostFreq[,1]))
      result <- mostFreq[1,1]
    }
    return (result)
  }
  
  NRisk <- getMedian(1)
  LRisk <- getMedian(2)
  VHRisk <- getMedian(3)
  MoRisk <- getMedian(4)
  HRisk <- getMedian(5)
  
  RiskCor <- data.frame(c(NRisk,LRisk,VHRisk,MoRisk,HRisk))
  RiskCor$rn <- c('NRisk','LRisk','VHRisk','MoRisk','HRisk')
  return(RiskCor)
}

#get topic correlation with risk level
l = Top100$Var1

l = c('gaming','aww')

GetAllCor <- function(topics, boostrapN){
  preCor = NULL
  mergeDf = NULL
  for (topic in topics){
    if (is.null(preCor) == F){
      CorRe <- GetTopicCor(topic, 'topic', boostrapN)
      colnames(CorRe) <- c(topic,'rn')
      mergeDf <- merge(preCor, CorRe, by ='rn', all= T)
      preCor <- mergeDf
    }
    else{
      CorRe <- GetTopicCor(topic, 'topic', boostrapN)
      colnames(CorRe) <- c(topic,'rn')
      preCor <- CorRe
    }
  }
  return(mergeDf)
  
}

system.time(allCor <- GetAllCor(l, 10))

#now we create the latex table
allCorLat <- data.frame(t(allCor))
allCorLat <- allCorLat[rowSums(is.na(allCorLat)) != ncol(allCorLat), ]
allCorLat <- allCorLat[,-6]
allCorLat[is.na(allCorLat)] <- 0
colnames(allCorLat) = allCorLat[1, ] # the first row will be the header
allCorLat <- allCorLat[-1, ]
colnames(allCorLat) <- c("data_HRisk","data_LRisk","data_MoRisk", "data_NRisk",  "data_VHRisk")

#convert to Latex table
ConvertNum <- function(df){
  for (i in colnames(df)){
    df[,c(i)] <- as.numeric(as.character(df[,c(i)]))
  }
  return (df)
}

allCorLat2 <- ConvertNum(allCorLat)
#allCorLat2 <- data.frame(sapply(allCorLat2, roundup))
setDT(allCorLat, keep.rownames = TRUE)[]
allCorLat2$subreddit<- allCorLat$rn

#stargazer(allCorLat2, type = 'latex',  summary=FALSE, out='/Users/lucia/phd_work/Clpsy/data/clpsych19_training_data/allCorLat2.csv', out.header=FALSE)

setwd(path)
writeWorksheetToFile("./suicideDetection/features/allCorLat2.xlsx", 
                     data = allCorLat2, 
                     sheet = "cor", 
                     header = TRUE,
                     clearSheets = TRUE)

