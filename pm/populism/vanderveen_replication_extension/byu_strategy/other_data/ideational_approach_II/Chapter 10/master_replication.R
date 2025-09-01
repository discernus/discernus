####################################################################
## author:    Robert Huber, Thomas Lehner and Carsten Wegscheider
######################################################################

#### Summary: This RScript combines all necessary data in a dataset with the unit of analysis "cabinet".
rm(list=ls())

## Load Packages that are not easy to feed directly
library(tidyverse)
library(ggthemes)
library(effects)

## set working directory and define personal folders with libraries

here::i_am("replication_materials.Rproj")

#### run scripts ####

source("rcode/descriptives_compliance.R")

source("rcode/analyses_compliance.R")

source("rcode/analyses_ches.R")
