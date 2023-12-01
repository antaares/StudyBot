from aiogram.dispatcher.filters.state import State, StatesGroup





class AdminState(StatesGroup):
    """States of admins"""

    # broadcast
    getMessage = State()
    Choice = State()
    Confirm = State()

    # manage admins
    AdminID = State()
    AdminName = State()
    ConfirmAdmin = State()

    # manage channels
    ForwardingMessage = State()


    # file manager
    GetFile = State()
    FileConfirm = State()
