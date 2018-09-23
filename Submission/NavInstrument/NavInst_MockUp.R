library("ggplot2")
library("ggmap")
library("readr")
library("dplyr")

# R: radius of the earth in nautical miles
R <- 0.53961 * 6371

# read data
### TODO conn to db

d <- read.csv("../../Data/subset.csv", row.names = 1)
d$time <-  as.POSIXct(d$BaseDateTime)
d$id =  factor(d$MMSI)


table(d$MMSI)


p = ggplot(d, aes(x=LON, y=LAT,color=time)) + geom_point()
p



d1 = tbl_df(d) %>%
  filter(LON < -123. &
           LON>-123.2 & 
           LAT >48.35 &
           LAT < 48.55) 
p = ggplot(d1, aes(x=LON, y=LAT,color=time, shape=id)) + geom_point()
p
ggsave(p, filename="twoship.pdf", width=6, height=4)



b1 = d1 %>%
  filter(id == 372883000) %>%
  arrange(time) %>%
  slice(1:15)

b2 = d1 %>%
  filter(id == 371782000) %>%
  arrange(time) %>%
  slice(7:21)

cbind(b1$time, b2$time, b1$time-  b2$time)


rel_pos = bind_cols(b1, b2) %>%
  mutate(r_lat = LAT - LAT1,
         r_lon = LON - LON1)
p = ggplot(rel_pos, aes(x = r_lat, y = r_lon, col=time)) + geom_point()
p
p + ylim(-0.020, 0.020) +  
  xlim(-0.025, 0.025)
  


##############################
d = data_frame(x1 = c(-500, 1000, -1000),
               y1= c(-1800, 2000, 500),
               x2=c(-1500, 1000, 500),
               y2 = c(0, 500, -500),
               status = c('green', 'green', 'red'),
               width = c(1,1,3))


plot(0,0, pch= 19, ylim = c(-2500, 2500), xlim=c(-2500, 2500),
     xlab='', ylab='', xaxt='n', yaxt='n',bty='n', 
     main = "Navigational Projections")
# plot(0,0, pch= 19, ylim = c(-2500, 2500), xlim=c(-2500, 2500),
#      xlab='', ylab='')
for(row in 1:nrow(d)){
  lines(x = c(d$x1[row], d$x2[row]), 
        y = c(d$y1[row], d$y2[row]),
        lwd=d$width[row], 
        col=d$status[row])
  points(x=d$x1[row], y=d$y1[row], pch=4, cex=2)
}

r = seq(0, 2*pi, length=300)
diam = c(500, 1000, 2000)
for(i in diam){
  points(i*cos(r), i*sin(r), type='l')
  text(x = i, y=0, as.character(i), pos=4, offset=0.25)
  }


