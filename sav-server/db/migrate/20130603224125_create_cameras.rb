class CreateCameras < ActiveRecord::Migration
  def change
    create_table :cameras do |t|
      t.string :url
      t.string :description
      t.integer :current_position
      t.string :go_to_position
      t.float :current_x_position
      t.float :current_y_position
      t.float :go_to_x_position
      t.float :go_to_y_position

      t.timestamps
    end
  end
end
