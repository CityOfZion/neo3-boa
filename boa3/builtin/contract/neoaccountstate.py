# from boa3.builtin.type import ECPoint
#
#
# class NeoAccountState:
#     """
#     Represents a transaction.
#
#     :ivar balance: the current account balance, which equals to the votes cast
#     :vartype balance: int
#     :ivar height: the height of the block where the balance changed last time
#     :vartype height: int
#     :ivar vote_to: the voting target of the account
#     :vartype vote_to: ECPoint
#     """
#
#     def __init__(self):
#         self.balance: int = 0
#         self.height: int = 0
#         self.vote_to: ECPoint = ECPoint(bytes(33))
