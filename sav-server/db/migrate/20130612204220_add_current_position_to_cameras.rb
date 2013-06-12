class AddCurrentPositionToCameras < ActiveRecord::Migration
  def change
    add_column :cameras, :current_position, :integer
  end
end
