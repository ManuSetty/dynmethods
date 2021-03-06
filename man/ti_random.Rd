% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/ti_random.R, R/ti_container.R
\name{ti_random}
\alias{ti_random}
\alias{ti_random}
\title{Inferring trajectories with Control: random}
\usage{
ti_random(docker = dynwrap::test_docker_installation(), dummy_param = 0.5)

ti_random(docker = dynwrap::test_docker_installation(), dummy_param = 0.5)
}
\arguments{
\item{docker}{Whether to use the docker container or the R wrapper}

\item{dummy_param}{This parameter does not do anything.}
}
\value{
The trajectory model
}
\description{
This control method will always produce a random trajectory.

Will generate a trajectory using Control: random. This method was wrapped inside a \href{https://github.com/dynverse/dynmethods/tree/master/containers/random}{container}.
}
\details{
This methods was first wrapped inside R, see \link{ti_random}
}
