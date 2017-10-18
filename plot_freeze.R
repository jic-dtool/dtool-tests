library("ggplot2")

df <- read.csv("freeze_timings.csv", header=T)
g <- ggplot(
      data=df,
      aes(x=num_files, y=time, group=code, colour=code)
)
g <- g + geom_line()
g <- g + geom_point()
g <- g + ylab("Time (s)")
g <- g + xlab("Number of 10 byte files")

ggsave("freeze_timings.png")
