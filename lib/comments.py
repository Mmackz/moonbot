from utils.utils import calculate_round_number

def moon_stats(total_karma, total_moon, ratio): 
    return f"""⚠️ **MOONs Security Information** ⚠️  
  
  - **Never share your 12 word backup. EVER!!**  
  - DM's are usually always a scam. Trade on legitimate exchanges only. (ie. Kraken🐙)  

&nbsp;  

📊 **Stats for this round** 📊  
  
   - Total Karma in this distribution: `~{total_karma}`  
   - Total MOON to be distributed: `~{round(total_moon)}`  
   - Ratio for this round: `~{round(ratio, 4)}`  

&nbsp;  

🌙 **Estimating your MOON distribution** 🌙  
  
> The formula is `Your Karma from CSV` * `{round(ratio, 4)}` 

You can comment `!lookup` in this thread to have u/_MoonBot look this up for you. Or you can use `!lookup username` to lookup another user.  
  
> **NOTE:**  *The total amount of Moons to be distributed won't be finalised until next week as 50% of the Moons burned from membership purchases are re-distributed in each round.*  

&nbsp;
  
🗳️ **Proposal Info** 🗳️  
  
Would you like to have a say in how MOONs get distributed? Come to r/CryptoCurrencyMeta where you can comment on pre-proposals, or submit your own proposal for comment.  

**Please check out r/CryptoCurrencyMeta for more info on the governance process.**  

&nbsp;  

📚 **Want to know more?** 📚  

Check out the [Moon Wiki](https://www.reddit.com/r/CryptoCurrency/wiki/moon) or visit the r/CryptoCurrencyMoons subreddit!
---  
  
^(I am a bot 🤖)"""

def info_reply(username, karma, ratio, moon):
    return f"""
**Round {calculate_round_number()} stats for {username}**

  - Total Karma: `{karma}` karma
  - Ratio: `{round(ratio, 4)}` 

Based on these stats, `u/{username}` should receive an estimated **~{moon} MOON** on distribution day. 

^(*estimate based on the snapshot data and is subject to change.*)
    
---
    
^(I am a bot 🤖)"""

def not_found(username):
    return f"""
`u/{username}` was not found in the snapshot data. Please try again with a different username.  

---
    
^(I am a bot 🤖)"""