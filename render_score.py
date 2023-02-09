import bpy, inspect

def main_script(scene):
    
    game_score_data = bpy.data.curves['GameScore_Number']
    high_score_data = bpy.data.curves['HighScore_Number']

    nb_objects_current_frame = 0
    
    game_score = 0
    game_score_data.body = '{:0>4}'.format(str(game_score))
    high_score_data.body = game_score_data.body
    
    i = 0
    
    print("========== FRAME:",bpy.context.scene.frame_current,"===========\n")

    print("========== GET VISIBLE ==========")
    for obj in bpy.data.objects:
        if obj.name.startswith("PAC-GOMME"):
            if obj.visible_get() == True:
                print(obj.name, "visible")
                nb_objects_current_frame += 1        
            else:
                print(obj.name, "not visible")
                game_score += 20
                game_score_data.body = '{:0>4}'.format(str(game_score))
                high_score_data.body = game_score_data.body
                
    
bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(main_script)