import copy

class Player7:

	def __init__(self):
		pass

	def find_heuristic(self, game_board):
		lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
		board = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
		he = 0
		for i in range(0, 9):
			ctr = 0
			block = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
			for j in range(i % 3 * 3, i % 3 * 3 + 3):
				for k in range(i / 3 * 3, i / 3 *3 + 3):
					block[ctr] = game_board[k][j]
					ctr += 1
			h = 0
			flag = 0
			for j in lines:
				ctr_x = 0
				ctr_o = 0
				for k in j:
					if block[k] == 'x':
						ctr_x += 1
					elif block[k] == 'o':
						ctr_o += 1
				if ctr_x == 1 and ctr_o == 0:
					h += 1
				if ctr_x == 2 and ctr_o == 0:
					h += 10
				if ctr_x == 3:
					h += 100
					flag = 1
				if ctr_o == 1 and ctr_x == 0:
					h -= 1
				if ctr_o == 2 and ctr_x == 0:
					h -= 10
				if ctr_o == 3:
					h -= 100
					flag = 1
			if block.count('x') + block.count('o') == 9 and flag == 0:
				board[i] = 'd'
			elif h > 0:
				board[i] = 'x'
			elif h < 0:
				board[i] = 'o'
			else:
				board[i] = '-'
			he += h
		H = 0
		flag = 0
		for i in lines:
			ctr_x = 0
			ctr_o = 0
			ctr_d = 0
			for j in i:
				if board[j] == 'x':
					ctr_x += 1
				elif board[j] == 'o':
					ctr_o += 1
				elif board[j] == 'd':
					ctr_d += 1
			if ctr_d == 0:
				if ctr_x == 1 and ctr_o == 0:
					H += 10
				if ctr_x == 2 and ctr_o == 0:
					H += 100
				if ctr_x == 3:
					H += 1000
					flag = 1
				if ctr_o == 1 and ctr_x == 0:
					H -= 10
				if ctr_o == 2 and ctr_x == 0:
					H -= 100
				if ctr_o == 3:
					H -= 1000
					flag = 1
		if block.count('x') + block.count('o') == 9 and flag == 0:
			H = 0
		H = H + he
		return H

	def move(self, board, block, old_move, flag):
		root = [None, [], board]
		root = self.generateTree(root, board, block, old_move, flag, 4)
		if flag == 'x':
			next = self.alphabeta(root, 4, -10000, 10000, True)
		else:
			next = self.alphabeta(root, 4, -10000, 10000, False)
		x = (next[1], next[2])
		return x

	def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
		if depth == 0 or node[1] == []:
			return node
		if maximizingPlayer:
			v = -10000
			maxchild = node
			for child in node[1]:
				v = max(v, self.alphabeta(child, depth - 1, alpha, beta, True)[0])
				if v > alpha:
					maxchild = child
				alpha = max(alpha, v)
				if beta <= alpha:
					break
			return [v, maxchild[3][0], maxchild[3][1]]
		else:
			v = 10000
			minchild = node
			for child in node[1]:
				v = min(v, self.alphabeta(child, depth - 1, alpha, beta, False)[0])
				if v < beta:
					minchild = child
				beta = min(beta, v)
				if beta <= alpha:
					break
			return [v, minchild[3][0], minchild[3][1]]

	def get_empty_out_of(self, gameb, blal, block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb / 3
			id2 = idb % 3
			for i in range(id1 * 3, id1 * 3 + 3):
				for j in range(id2 * 3, id2 * 3 + 3):
					if gameb[i][j] == '-':
						cells.append((i, j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			for i in range(9):
				for j in range(9):
					no = (i/3)*3
					no += (j/3)
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))	
		return cells

	def generateTree(self, node, board, block_stat, old_move, flag, depth):
		if depth == 0:
			return node

		for_corner = [0,2,3,5,6,8]

		blocks_allowed  = []

		if old_move[0] == -1 and old_move[1] == -1:
			blocks_allowed = [0, 1, 2, 3, 4, 5 ,6, 7, 8]
		elif old_move[0] in for_corner and old_move[1] in for_corner:
			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				blocks_allowed = [1]
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				blocks_allowed = [3]
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				blocks_allowed = [7]
			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

		for j in reversed(blocks_allowed):
			if block_stat[j] != '-':
				blocks_allowed.remove(j)

		cells = self.get_empty_out_of(board, blocks_allowed, block_stat)

		game_board = copy.deepcopy(board)
		block = copy.deepcopy(block_stat)
		fl = flag
		children = []

		for move_ret in cells:
			fl = flag
			game_board = copy.deepcopy(board)
			block = copy.deepcopy(block_stat)
			game_board[move_ret[0]][move_ret[1]] = fl
			#print "move:", move_ret, "block:", block_stat

			block_no = (move_ret[0] / 3) * 3 + move_ret[1] / 3
			id1 = block_no / 3
			id2 = block_no % 3
			mg = 0
			mflg = 0
			if block[block_no] == '-':
				if game_board[id1 * 3][id2 * 3] == game_board[id1 * 3 + 1][id2 * 3 + 1] and game_board[id1 * 3 + 1][id2 * 3 + 1] == game_board[id1 * 3 + 2][id2 * 3 + 2] and game_board[id1 * 3 + 1][id2 * 3 + 1] != '-':
					mflg=1
				if game_board[id1 * 3 + 2][id2 * 3] == game_board[id1 * 3 + 1][id2 * 3 + 1] and game_board[id1 * 3 + 1][id2 * 3 + 1] == game_board[id1 * 3][id2 * 3 + 2] and game_board[id1 * 3 + 1][id2 * 3 + 1] != '-':
					mflg=1
		
                	if mflg != 1:
                   		for i in range(id2 * 3, id2 * 3 + 3):
                   			if game_board[id1 * 3][i] == game_board[id1 * 3 + 1][i] and game_board[id1 * 3 + 1][i] == game_board[id1 * 3 + 2][i] and game_board[id1 * 3][i] != '-':
                   				mflg = 1
                   				break
				if mflg != 1:
					for i in range(id1 * 3, id1 * 3 + 3):
						if game_board[i][id2 * 3] == game_board[i][id2 * 3 + 1] and game_board[i][id2 * 3 + 1] == game_board[i][id2 * 3 + 2] and game_board[i][id2 * 3] != '-':
							mflg = 1
							break
			if mflg == 1:
				block[block_no] = fl
	
        		#check for draw on the block.

        		id1 = block_no/3
			id2 = block_no%3
        		cell = []
			for i in range(id1 * 3, id1 * 3 + 3):
				for k in range(id2 * 3, id2 * 3 + 3):
					if game_board[i][k] == '-':
						cell.append((i, k))

				if cell == [] and mflg != 1:
					block[block_no] = 'd'
			
			if fl == 'x':
				fl = 'o'
			else:
				fl = 'x'
			
			if depth != 1:
				child = [None, [], game_board, move_ret]
			else:
				h = self.find_heuristic(game_board)
				#print game_board
				#print move_ret
				child = [h, [], game_board, move_ret]
			c = self.generateTree(child, game_board, block, move_ret, fl, depth - 1)
			children.append(c)
		node[1] = children
		return node
