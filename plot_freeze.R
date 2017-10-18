library("ggplot2")

df <- read.csv("example.csv", header=T)
g <- ggplot(
      data=df,
      aes(x=num_files, y=time, group=code, colour=code)
)
g <- g + geom_line()

ggsave("freeze_timings.png")
