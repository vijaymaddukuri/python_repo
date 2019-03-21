def MergeLists(headA, headB):
    if headA is None and headB is None:
        return None

    if headA is None:
        return headB

    if headB is None:
        return headA

    if headA.data < headB.data:
        smallerNode = headA
        smallerNode.next = MergeLists(headA.next, headB)
    else:
        smallerNode = headB
        smallerNode.next = MergeLists(headA, headB.next)

    return smallerNode

def MergeListsNonRecursive(headA, headB):
    if not headA or not headB:
        return headA or headB

    if min([headA.data, headB.data]) == headA.data:
        head, headA, headB = (headA, headA.next, headB)
    else:
        head, headA, headB = headB, headA, headB.next

    curr = head
    while headA or headB:

        if not headA or not headB:
            curr.next = headA or headB
            return head

        curr.next, headA, headB = (headA, headA.next, headB) \
            if min([headA.data, headB.data]) == headA.data \
            else (headB, headA, headB.next)
        curr = curr.next
    return head