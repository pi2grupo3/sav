class CreateCameras < ActiveRecord::Migration
  def change
    create_table :cameras do |t|
      t.float :batery_state
      t.string :current_position
      t.string :go_to_position
      t.float :current_x_position
      t.float :current_y_position
      t.float :go_to_x_position
      t.float :go_to_y_position

      t.timestamps
    end
  end
end
