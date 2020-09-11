# What is this?
If you don't know what the iTech opportunity matrix is then this isn't for you and wont be of much interest! 

Long story short this loops through the Opportunity Matrix as a csv, identifies any instances where your site has dipped in visibility based on best reported rank, then tries to map other network rankings to your URLs based on shared keyword rankings. It will get things wrong, but it will do things faster than manually. The second script will loop through unknown-keywords file to find otherwise mapped content, and then create a list of rankings that aren't known to your site, or found in your keyword gap file.

## Enough Jammering How Do I Use It?
* Go download the  *GECKOpportunity Matrix - Autumn 2020.xlsx* and save the *Master* tab as a csv (I call it geckos.csv but you can specify this in the config.ini file)
* specify your domain *as it appears in the GECKOpportunity Matrix* in the config.ini file
* OPTIONALLY specify your own site CTR (the provided relates to CORG August 19 - July 20)
* Install python3 and the script dependancies (pandas, configparser)
* Double click on *GKWM.py*
* Manually edit *Unknown-Keywords.csv* deleting anything you don't consider relevant to the page mapped/update to reflect the correct URL. Save changes
* Double click on *FUC.py*
* Pivot *Unknown-Content.csv* to identify new content opportunities

## This is Cool Can We Do Something Similar For Ahrefs/SEMrush?
Yes that's a good idea. Please provide John with feedback/suggestions etc.

## This Is Crap And Someone Should Unplug Your Keyboard
Very true. Want to help improve it? Submit a pull request!