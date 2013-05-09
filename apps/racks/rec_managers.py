from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from common import utils
from voting.models import Vote
from tagging.models import Tag
from tagging.managers import ModelTaggedItemManager

class RecommenderManager(ModelTaggedItemManager):

    MIN_RECOMMENDATION_VALUE = 0
    MIN_SIMILARITY_VALUE = 0.01
    MIN_CONTENT_BASED_RECOMMENDATION_VALUE = 0.01

    
    def get_best_items_for_user(self, user, user_list, item_list, min_value=MIN_RECOMMENDATION_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)

        recs = utils.get_usb_recommendations(user.id, user_item_matrix)
        recs.sort(reverse=True)
        
        items = [(value, self.get(id = rec)) for value,rec in recs if value>min_value]

        return items
        
    def get_similar_items(self, item, user_list, item_list, min_value=MIN_SIMILARITY_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        item_user_matrix = self.rotate_matrix(user_item_matrix)
        sim_list = []
        for other in item_list:
            if item==other:continue
            sim=utils.distance_matrix_p1_p2(item_user_matrix[item.id],item_user_matrix[other.id]) #returns a 0..1 value
            if sim>min_value:
                sim_list.append((sim,other))
            
        sim_list.sort(reverse=True)
        return sim_list
        
    def create_matrix(self, users, items):
        user_item_matrix = {}
        for user in users:
            votes_for_user = Vote.objects.get_for_user_in_bulk(items, user)
            user_item_matrix[user.id] = votes_for_user
        
        return user_item_matrix
    
    def rotate_matrix(self, matrix):
        rotated_matrix = {}
        for user in matrix:
            for item in matrix[user]:
                rotated_matrix.setdefault(item,{})
                rotated_matrix[item][user]=matrix[user][item]
        return rotated_matrix
        

    def get_content_based_recs(self, user, tagged_items, min_value=MIN_CONTENT_BASED_RECOMMENDATION_VALUE):

        item_tag_matrix = {}
        for item in tagged_items:
            item_tag_matrix[item] = Tag.objects.get_for_object(item)
        
        user_tags = Tag.objects.get_for_object(user)
        
        recs = []
        for item,item_tags in item_tag_matrix.items():
            sim = utils.tanamoto2(item_tags, user_tags)
            if sim>=min_value:
                recs.append((sim, item))
                
        return recs

    

