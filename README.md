Feature Toggles
=======
Feature Toggles (also known as Feature Flags, Feature Flippers, or Feature Switches) consist on surrounding 
features (functionalities) in the code with if statements to gain more control over their release process. 
By surrounding a feature with a toggle (if statement), developers can decide when and for whom 
the feature should be available. 

This repository contains all data used for the research described in the paper.

Paper
=======
How the adoption of feature toggles may affect the branching merge process and bugs in open-source projects?

Content
=======
Spreadsheets and R Scripts that were used to perform the all the analysis of this paper.

Guide
=======

Corpus Compose for each research question:
	
	The totally of the projects is listed on the "resumo" spreadsheet (git.xlsx). This spreadsheet concentrates all data needed to perform all the research question's analysis. 

	1) Research Question 1:
	 
		The git.xlsx ("resumo" spreadsheet) represents the result of the queries, on Github, for projects that adopted feature toggles.
	
	2) Research Question 2:
		
		The filter_RQ_2.xlsx represents the totally of projects that show at least one merge commit.
	
	3) Research Question 3:
		
		The filter_RQ_3.xlsx represents the totally of projects that show at least one issue or pull request representing a bug.
		
Corpus Filter:

	1) Research Question 1:
	
		No further action to apply a filter.
	
	2) Research Question 2:
	
		To calculate de the threshold, we ran the R script on filter_RQ2.txt.
		Based on filter_RQ_2, we applied a filter with 82 commits, before and after feature toggles (qtde_commit_s_fw and qtde_commit_c_fw).
		The result of this selection is CRQ2.xlsx.
	
	3) Research Question 3:
	
		To calculate de the threshold, we ran the R script on filter_RQ3.txt.
		Based on filter_RQ_3, we applied a filter with 132 commits, before and after feature toggles (qtde_commit_s_fw and qtde_commit_c_fw).
		The result of this selection is CRQ3.xlsx.

Research Question's Analysis:

	1) Research Question 1:
	
		The analysis of the average moment of adoption for each programming language are described on dispersao.xlsx
		
	2) Research Question 2:
		
		a) RQ 2.1:			
			To obtain the results of the analysis RQ 2.1, we ran in R Studio, described on RQ2_1.txt;
			Scatter plot script is described on RQ_2_1_scatter_plot.txt;
			To perform the analysis for each programming language, we ran in R Studio, the RQ2_1_PROGLAN.txt.
		
		b) RQ 2.2:						
			On analysis over the RQ 2.2 e 2.3, we created a new corpus, derived of CRQ2.xlsx, with only projects with at least one merge commit.
			To obtain the results of the analysis RQ 2.2, we ran in R Studio, described on RQ2_2.txt;
		
		c) RQ 2.3:									
			To obtain the results of the analysis RQ 2.3, we ran in R Studio, described on RQ2_3.txt;
	
	3) Research Question 3:
	
		a) RQ 3.1:			
			To obtain the results of the analysis RQ 3.1, we ran in R Studio, described on RQ3_1.txt;						
		
		b) RQ 3.2:						
			On analysis over the RQ 3.2 e 3.3, we created a new corpus, derived of CRQ3.xlsx, with only projects with at least one bug issues or pull request.
			To obtain the results of the analysis RQ 3.2, we ran in R Studio, described on RQ3_2.txt;		
		
		c) RQ 3.3:									
			To obtain the results of the analysis RQ 3.3, we ran in R Studio, described on RQ3_3.txt;
	
	
