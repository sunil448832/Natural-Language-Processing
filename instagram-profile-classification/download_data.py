import instaloader
import os
import shutil

# Creating an instance of the Instaloader class
bot = instaloader.Instaloader()
def download_profile(instagram_link):
  user_name=instagram_link.replace('https://www.instagram.com/','').split('/')[0]
  # Loading the profile from an Instagram handle
  profile = instaloader.Profile.from_username(bot.context, user_name)
  #print(profile)
  print("Username: ", profile.username)
  print("Bio: ", profile.biography)
  posts = profile.get_posts()


  # Iterating and downloading all the individual posts
  save_dir='data'
  os.makedirs(save_dir, exist_ok=True)
  os.chdir(save_dir)
  for index, post in enumerate(posts, 1):
    bot.download_post(post, target=f'{user_name}_{index}')
    if index>10:break
  os.chdir('../')

  documents=[]
  for dirs in os.listdir(save_dir):
    dirs_path=os.path.join(save_dir,dirs)
    for file_name in os.listdir(dirs_path):
      if file_name.endswith('.txt'):
        file_path = os.path.join(dirs_path, file_name)
        with open(file_path, 'r') as file:
            content = file.read()
            documents.append(content)
  shutil.rmtree(save_dir)
  return documents

# documents=download_profile('https://www.instagram.com/divya_pawar8511/?next=%2F')
# print("Doc-------------",documents)
