class CurrentPositionChangedToInteger < ActiveRecord::Migration
  def up
    change_table :cameras do |t|
      t.remove :current_position
    end
  end

  def down
    change_table :cameras do |t|
      t.string :current_position
    end
  end
end
