#---------------------------------------#
#          stat.R v2.6 2D               #
#---------------------------------------#
# Statistical post processing for Lotus #
#---------------------------------------#
#  Opens the various utputs from Lotus
# Stat commands. Filters them and
# calculates the statistical properties
# of them. Finally creates the .pdf
# images that form the report.
#---------------------------------------#
#  Version notes:
# v1.0: first stat.R given
# v2.0: Added filtering parameters
#             Cl output
# v2.5: Added Cd output
#             some morecomments
# v2.6: Centered the text in the
#  filtered region.
#---------------------------------------#
#
# loading libraries
library(dplyr);library(ggplot2)
#
# read data from
data = read.table("fort.9",
                  #col.names = c("time","CFL","drag","lift","pforceZ","dragf","liftf","vforceZ"))
                  col.names = c("time","CFL","drag","lift","dragf","liftf"))
#
# calculate statistical properties between filtering limits
# signal filterig limits (fraction of the total time)
xLowerFilter = 0.8
xUpperFilter = 1
#
easy = data %>% filter(time>xLowerFilter*(max(time)-min(time))+min(time)) %>%
  filter(time<xUpperFilter*max(time)) %>%
  summarize(t =  0.5*(max(time)-min(time))+min(time),
            mdrag = mean(drag+dragf), mlift = mean(lift+liftf),
            adrag = mad(drag+dragf), alift = mad(lift+liftf),
            rmsdrag = sqrt(mean((drag+dragf)^2)),
            rmslift = sqrt(mean((lift+liftf)^2)),
            ndrag = 1.2*min(drag), nlift=1.2*min(lift)
  )
attach(easy)
#
# subsample data to reduce the sice of the report
l = length(data$time)
n = 2000
j = round(seq(5,l,len=min(l,n)))
data = data[j,]
#
# cfl plot
CFL = qplot(time,CFL,data=subset(data,CFL<1),geom="line")
#
# drag plot
data$drag[data$time<1] = mdrag
drag = qplot(time,drag,data=data,geom="line") +
  geom_line(aes(y=dragf),color='red') +
  geom_vline(xintercept = xLowerFilter*(max(data$time)-min(data$time))+min(data$time),color='gray') + geom_vline(xintercept = xUpperFilter*max(data$time),color='gray')
drag = drag+annotate("text",x=t,y=ndrag,label=paste("mean=",round(mdrag,3)," amp=",round(adrag,3)),check_overlap = TRUE )
#
# lift plot
lift = qplot(time,lift,data=data,geom="line") +
  geom_line(aes(y=liftf),color='red') +
  geom_vline(xintercept = xLowerFilter*(max(data$time)-min(data$time))+min(data$time),color='gray') + geom_vline(xintercept = xUpperFilter*max(data$time),color='gray')
lift = lift+annotate("text",x=t,y=nlift,label=paste("mean=",round(mlift,3)," amp=",round(alift,3),"rms=",round(rmslift,3)))
#
#
ppdf = function(plot,name){
     # function that generates a pdf figure given an plot and a name
     pdf(name,8,4)
     print(plot)
     dev.off()
}
#
# create pdf figures for the cfl, drag and lift
ppdf(CFL,"11CFL.pdf")
ppdf(drag,"01drag.pdf")
ppdf(lift,"02lift.pdf")
#
# read data from fort.8 after being turned to mgs.txt by the runStat script
data = read.table("mgs.txt", col.names = c("itr","res"))
#
# resamplt it
l = length(data$itr)
n = 2000
data$i = seq(1,l)
j = round(seq(1,l,len=min(l,n)))
#j = unique(c(which(data$itr>1),j))
data = data[j,]
#
# plot it and create pdf figures
itr = qplot(i,log(itr,2),data=data)+ylab(expression(log[2](iteration)))
res = qplot(i,log(res,10),data=data)+ylab(expression(log[10](residual)))
ppdf(itr,"13itr.pdf")
ppdf(res,"12res.pdf")
#
try(source('analysis.R'))
#
# wrtite to a file the Cl data.
# mean, amplitude, root mean squared
write(c(mlift,alift,rmslift), file = "clDat.csv", sep = ",")
#
# wrtite to a file the Cd data.
# mean, amplitude, root mean squared
write(c(mdrag,adrag,rmsdrag), file = "cdDat.csv", sep = ",")
#
#--- end of stat.R ---#
