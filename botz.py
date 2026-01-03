from data import bot, db
import handlers


if __name__ == '__main__':
    db.create_table_avto_tigach()
    db.create_table_county()
    db.create_table_driver()
    # db.delete_table_fuel_output()
    db.create_table_fuel_output()
    bot.infinity_polling()
