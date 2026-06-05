-- ========================================================
-- SignSpeak Initial Seed Data
-- ========================================================

INSERT INTO vocabulary_signs (symbol, label, category, description, tips) VALUES
('A', 'Letter A', 'alphabet', 'Closed fist with thumb resting vertically against the side of the index finger.', 'Keep thumb straight up beside the index finger.'),
('B', 'Letter B', 'alphabet', 'Four fingers held straight and upright together, thumb tucked horizontally across palm.', 'Keep the four fingers pressed tightly together.'),
('C', 'Letter C', 'alphabet', 'Hand curved into a C shape resembling the letter.', 'Cup your fingers smoothly with thumb opposing.'),
('D', 'Letter D', 'alphabet', 'Index finger pointing upright, other fingers curled touching the thumb in a circle.', 'Only the index finger is extended.'),
('E', 'Letter E', 'alphabet', 'Fingers curled inward with tips resting on top edge of tucked thumb.', 'Do not form a full fist; fingertips touch thumb.'),
('F', 'Letter F', 'alphabet', 'Index finger and thumb touch tips in a circle (like OK), three other fingers spread upright.', 'Middle, ring, and pinky point straight up.'),
('G', 'Letter G', 'alphabet', 'Index finger and thumb extended horizontally parallel to each other.', 'Point horizontally across your chest.'),
('H', 'Letter H', 'alphabet', 'Index and middle fingers extended together horizontally.', 'Keep index and middle fingers touching.'),
('I', 'Letter I', 'alphabet', 'Pinky finger held upright, other fingers closed in a fist.', 'Thumb locks over other three fingers.'),
('K', 'Letter K', 'alphabet', 'Index pointing up, middle finger pointing forward, thumb tucked between them.', 'Thumb knuckle touches middle finger.'),
('L', 'Letter L', 'alphabet', 'Thumb and index finger form an L angle.', 'Form a crisp 90-degree angle.'),
('M', 'Letter M', 'alphabet', 'Three fingers folded over thumb.', 'Thumb peeks out between ring and pinky.'),
('N', 'Letter N', 'alphabet', 'Two fingers folded over thumb.', 'Thumb peeks out between middle and ring.'),
('O', 'Letter O', 'alphabet', 'All fingertips curve to touch thumb tip, forming an O.', 'Round out the shape.'),
('P', 'Letter P', 'alphabet', 'Like K but pointed downward toward the ground.', 'Index points down, middle forward-down.'),
('Q', 'Letter Q', 'alphabet', 'Like G pointing downward.', 'Thumb and index point toward the floor.'),
('R', 'Letter R', 'alphabet', 'Index and middle fingers crossed.', 'Middle finger wraps around front of index.'),
('S', 'Letter S', 'alphabet', 'Fist with thumb wrapped across all fingers.', 'Different from A: thumb crosses over fingers.'),
('T', 'Letter T', 'alphabet', 'Fist with thumb inserted between index and middle fingers.', 'Thumb tip pops up between first two fingers.'),
('U', 'Letter U', 'alphabet', 'Index and middle fingers pointing straight up together.', 'Fingers must touch.'),
('V', 'Letter V', 'alphabet', 'Index and middle fingers pointing up in a V / Peace shape.', 'Spread index and middle apart.'),
('W', 'Letter W', 'alphabet', 'Index, middle, and ring fingers spread upright.', 'Three fingers open in a W.'),
('X', 'Letter X', 'alphabet', 'Curled hook with index finger, rest of fingers closed.', 'Think of a pirates hook.'),
('Y', 'Letter Y', 'alphabet', 'Thumb and pinky extended, middle three fingers folded.', 'The classic hang loose hand gesture.'),
('SPACE', 'Space / Word Break', 'control', 'Flat palm gesture indicating a word boundary.', 'Used by the sentence builder to add a space.'),
('BACKSPACE', 'Backspace', 'control', 'Fist pointing thumb leftwards to delete the last character.', 'Deletes the preceding letter.'),
('CLEAR', 'Clear Text', 'control', 'Horizontal swipe gesture to clear the current sentence.', 'Resets the sentence transcript.'),
('HELLO', 'Hello', 'word', 'Flat open hand raised near temple/shoulder.', 'A friendly open wave or salute.'),
('THANK_YOU', 'Thank You', 'word', 'Flat hand moving from chin forward.', 'Fingertips start near lips and move outward.'),
('YES', 'Yes', 'word', 'Closed fist mimicking a nodding head.', 'Nod fist up and down gently.'),
('NO', 'No', 'word', 'Index and middle fingers snapping down to touch thumb.', 'Quick closure like a talking bird beak.'),
('I_LOVE_YOU', 'I Love You', 'word', 'Thumb, index, and pinky extended together (ASL ILY).', 'Combines I, L, and Y into one gesture.')
ON CONFLICT (symbol) DO NOTHING;
