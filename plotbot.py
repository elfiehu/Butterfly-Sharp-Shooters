def twitter_req(last_id):
    #global last_id
    """Finds requested twitter account"""
    plotbot = "@PlotBot24"
    # Search for all tweets
    public_tweets = api.search(plotbot, count = 100, result_type='recent', since_id=last_id)
    
    # First, check if there are any new tweets
    if public_tweets['statuses']:
        
        # Loop through all tweets
        for tweet in public_tweets['statuses']:
            
            # Get target twitter account from request status
            tweet_author = tweet["user"]["screen_name"]
            tweet_text = tweet['text']
            new_target = tweet_text[20:]
            print(f"Tweet Author: {tweet_author}")
            last_id = int(tweet['id'])
            last_id += 1
            return new_target
    else:
        return False
def s_analyze(new_target):
    """Perform sentiment analysis on requested account"""
    counter = 1
    sentiments = []
    tweet_times = []
    
    # If target twitter account is not in the the accounts list, 
    # then append it and perform a sentiment analysis
    if new_target not in accounts:
        accounts.append(new_target)
        
        for x in range(5):
                    
            public_tweets = api.user_timeline(new_target, page=x)
                    
            for tweet in public_tweets:
                        
                results = analyzer.polarity_scores(tweet['text'])
                compound = results['compound']
                pos = results['pos']
                neu = results['neu']
                neg = results ['neg']
                tweets_ago = counter
                date = tweet['created_at']
                    
                sentiments.append({"Compound": compound,
                                "Negative": neg,
                                "Neutral": neu,
                                "Positive": pos,
                                "Tweets Ago": tweets_ago,
                                "Date": date})
                counter += 1
                
            # Create dataframe from sentiments dictionary
            sentiments_pd = pd.DataFrame(sentiments)
            plot_report(sentiments_pd)
            
    else: 
        msg = f"Oops: No new requests. {new_target} already analyzed."
        print(msg)
def plot_report(data):
    okay = twitter_req(last_id)
    # Create plot
    plt.plot(-np.arange(len(data["Compound"])),data["Compound"], marker="o", color='maroon', linewidth=0.2, alpha=0.75)

    # Incorporate the other graph properties
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    plt.title("Sentiment Analysis of Tweets ({}) for {}".format(now, okay))
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    plt.xlim([-len(sentiments_pd['Compound'])-7, 7])
    plt.ylim([-1.05, 1.05])
    plt.grid(True)
    
    plt.savefig(f"{okay}_sentiment_analysis.png")

    #api.update_with_media(f"{new_target}_sentiment_analysis.png",
    print(f"New Tweet Analysis: {okay}")
    print(accounts)
    plt.show()
# Set timer to run every 5 minutes for 24 hours
t_end = time.time() + 3600 * 24
accounts = ["False"]
last_id = None
while(time.time() < t_end):
    r = twitter_req(last_id)
    s_analyze(r)
    time.sleep(100)
def s_analyze(new_target):
    """Perform sentiment analysis on requested account"""
#     plotbot = "@PlotBot24"

#     # Search for most recent mention
#     public_tweets = api.search(plotbot, count=1, result_type='recent')
#     if (public_tweets['statuses']):
#         for tweet in public_tweets['statuses']:

#         # Get target twitter account from request status
#             tweet_author = tweet["user"]["screen_name"]
#             new_target = f"@{tweet['entities']['user_mentions'][1]['screen_name']}"
#         # Originally did: tweet_text = tweet['text']\n new_target = tweet_text[20:], but above line of code is safer 

#         # Debug statement
#             print(f"Tweet Author: {tweet_author}")
#         #return new_target
#     else:
#         print("No new tweets.")
    # Set a counter and lists to hold sentiment data retrieved
    counter = 1
    sentiments = []
    tweet_times = []
    
    # If target twitter account is NOT in the the accounts list, append it
    if new_target not in accounts:
        
        accounts.append(new_target)
        
        # Then, search through user's timeline for 500 tweets
        # Note: Each page is 20 tweets, so we need 25 pages for 500 tweets
        for x in range(25):      
            public_tweets = api.user_timeline(new_target, page=x)
            
            # Perform sentiment analysis on tweets
            for tweet in public_tweets:
                results = analyzer.polarity_scores(tweet['text'])
                compound = results['compound']
                pos = results['pos']
                neu = results['neu']
                neg = results ['neg']
                tweets_ago = counter
                date = tweet['created_at']
                
                # Append sentiment data to sentiments list as a dictionary
                sentiments.append({"Compound": compound,
                                "Negative": neg,
                                "Neutral": neu,
                                "Positive": pos,
                                "Tweets Ago": tweets_ago,
                                "Date": date})
                
                # Add one to the counter
                counter += 1
                
        # Create dataframe from sentiments dictionary
        sentiments_pd = pd.DataFrame(sentiments)
        
        # Plot the sentiments data frame
        plt.plot(-np.arange(len(sentiments_pd["Compound"])),sentiments_pd["Compound"], marker="o", 
                 color='steelblue', markersize=5, linewidth=0.2, alpha=0.65, label=f"{new_target}")
        
        # Incorporate the other graph properties
        now = datetime.now()
        now = now.strftime("%Y-%m-%d")
        plt.title("Sentiment Analysis of Tweets ({})".format(now), fontdict={'fontsize':12})
        plt.ylabel("Tweet Polarity")
        plt.xlabel("Tweets Ago")
        plt.xlim([-len(sentiments_pd['Compound'])-10, 10])
        plt.ylim([-1.05, 1.05])
        plt.tick_params(bottom='off', left='off')
        plt.yticks(np.arange(-1,1.05, 0.5))
        
        lgd = plt.legend(fontsize='small', mode='Expanded', 
                   numpoints=1,scatterpoints=1,loc='upper left', 
                   bbox_to_anchor=(1,1), facecolor='white',
                   edgecolor='white', title='Tweets')
        
        # Save figure as a picture so we can use it as media 
        plt.savefig(f"{new_target}_sentiment_analysis.png", bbox_extra_artists=(lgd,), bbox_inches='tight')
        
        # Update status on @PlotBot24 with analysis media
        api.update_with_media(f"{new_target}_sentiment_analysis.png", 
                              f"New Tweet Analysis: {new_target}")
        
        # Debug statements
        print(f"New Tweet Analysis: {new_target}")
        print(accounts)
        return plt.show()
            
    else: 
        msg = f"Oops: No new requests. {new_target} already analyzed."
        print(msg)