class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @staticmethod
    def from_list(arr: list):
        """
        Convert an array to a linked-list, and return the head of the linked-list (for testing purposes).
        """
        head = None
        prev = None
        for element in arr:
            cur = ListNode(element)
            if not head:
                # Set the head to the first element
                head = cur
            else:
                prev.next = cur
            prev = cur
        return head

    def to_list(self):
        """
        Convert this linked-list into an array (for testing purposes).
        """
        arr = []
        cur = self
        while cur:
            arr.append(cur.val)
            cur = cur.next
        return arr
